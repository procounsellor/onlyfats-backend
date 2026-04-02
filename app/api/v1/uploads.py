import re
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.creator import Creator
from app.services.upload_service import upload_file_to_gcs

router = APIRouter()

VALID_PURPOSES = {"user_profile", "creator_profile", "post_media"}


@router.post("/uploads")
async def upload_files(
    purpose: str = Form(..., description="user_profile | creator_profile | post_media"),
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if purpose not in VALID_PURPOSES:
        raise HTTPException(status_code=400, detail=f"Invalid purpose. Must be one of: {', '.join(sorted(VALID_PURPOSES))}")

    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    creator_id = None
    if purpose in {"creator_profile", "post_media"}:
        result = await db.execute(
            select(Creator).where(Creator.user_id == current_user.id, Creator.is_active == True)
        )
        creator = result.scalar_one_or_none()
        if not creator:
            raise HTTPException(status_code=404, detail="Creator profile not found")
        creator_id = creator.id

    uploaded = []
    for file in files:
        if not file or not file.filename:
            continue
        try:
            item = await upload_file_to_gcs(
                bucket_name=settings.GCS_BUCKET_NAME,
                purpose=purpose,
                user_id=current_user.id,
                creator_id=creator_id,
                file=file,
            )
            uploaded.append(item)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed for {file.filename}: {str(e)}")

    if not uploaded:
        raise HTTPException(status_code=400, detail="No valid files were uploaded")

    return {"status": True, "message": "Files uploaded successfully", "data": uploaded}


@router.get("/media/{object_path:path}")
async def serve_media(object_path: str, request: Request):
    """
    Serve a GCS object with range-request support for fast video streaming.
    Tries a signed-URL redirect first (browser streams directly from GCS CDN).
    Falls back to range-aware proxy if signing is unavailable.
    """
    from google.cloud import storage

    def _load_blob():
        client = storage.Client()
        bucket = client.bucket(settings.GCS_BUCKET_NAME)
        blob = bucket.blob(object_path)
        blob.reload()
        return blob, blob.content_type or "application/octet-stream", blob.size

    try:
        blob, content_type, total_size = await run_in_threadpool(_load_blob)
    except Exception:
        raise HTTPException(status_code=404, detail="Media not found")

    # ── Try signed-URL redirect (browser streams directly from GCS CDN) ──────
    def _signed_url():
        return blob.generate_signed_url(
            expiration=timedelta(hours=1),
            method="GET",
            version="v4",
        )

    try:
        signed_url = await run_in_threadpool(_signed_url)
        return RedirectResponse(url=signed_url, status_code=302)
    except Exception:
        pass  # signing not available — fall through to range proxy

    # ── Range-aware proxy fallback ────────────────────────────────────────────
    range_header = request.headers.get("range")

    if range_header and total_size:
        m = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else total_size - 1
            end = min(end, total_size - 1)

            def _download_range():
                return blob.download_as_bytes(start=start, end=end)

            data = await run_in_threadpool(_download_range)
            return Response(
                content=data,
                status_code=206,
                media_type=content_type,
                headers={
                    "Content-Range": f"bytes {start}-{end}/{total_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(len(data)),
                    "Cache-Control": "private, max-age=3600",
                },
            )

    # Full file (images / small files)
    def _download_all():
        return blob.download_as_bytes()

    data = await run_in_threadpool(_download_all)
    return Response(
        content=data,
        media_type=content_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(total_size),
            "Cache-Control": "private, max-age=3600",
        },
    )
