from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.schemas.creator import CreateOrUpdateCreatorProfileRequest
from app.services.creator_service import create_or_update_creator_profile, get_creator_by_user_id

# use your real get_db import here
from app.core.database import get_db

router = APIRouter(tags=["Creator Profile"])


@router.post("/me")
async def create_or_update_my_creator_profile(
    request: CreateOrUpdateCreatorProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    creator = await create_or_update_creator_profile(db, current_user.id, request)
    return {
        "status": True,
        "message": "Creator profile saved successfully",
        "data": {
            "creator_id": creator.id,
            "user_id": creator.user_id,
            "display_name": creator.display_name,
            "bio": creator.bio,
            "profile_image_url": creator.profile_image_url,
            "is_active": creator.is_active
        }
    }


@router.get("/me")
async def get_my_creator_profile(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    creator = await get_creator_by_user_id(db, current_user.id)
    if not creator:
        raise HTTPException(status_code=404, detail="Creator profile not found")

    return {
        "status": True,
        "data": {
            "creator_id": creator.id,
            "user_id": creator.user_id,
            "display_name": creator.display_name,
            "bio": creator.bio,
            "profile_image_url": creator.profile_image_url,
            "is_active": creator.is_active
        }
    }