from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
async def serve_media(
    object_path: str,
):
    """Stream a GCS object. Paths are UUID-based so not guessable."""
    try:
        from google.cloud import storage
        from fastapi.responses import StreamingResponse
        from starlette.concurrency import run_in_threadpool
        import io

        def _download():
            client = storage.Client()
            bucket = client.bucket(settings.GCS_BUCKET_NAME)
            blob = bucket.blob(object_path)
            data = blob.download_as_bytes()
            return data, blob.content_type or "application/octet-stream"

        data, content_type = await run_in_threadpool(_download)
        return StreamingResponse(io.BytesIO(data), media_type=content_type)
    except Exception:
        raise HTTPException(status_code=404, detail="Media not found")
