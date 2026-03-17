from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.creator import Creator
from app.schemas.creator import CreateOrUpdateCreatorProfileRequest


async def get_creator_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Creator).where(Creator.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_or_update_creator_profile(
    db: AsyncSession,
    user_id: int,
    request: CreateOrUpdateCreatorProfileRequest
):
    creator = await get_creator_by_user_id(db, user_id)

    if creator:
        creator.display_name = request.display_name
        creator.bio = request.bio
        creator.profile_image_url = request.profile_image_url
    else:
        creator = Creator(
            user_id=user_id,
            display_name=request.display_name,
            bio=request.bio,
            profile_image_url=request.profile_image_url,
            is_active=True
        )
        db.add(creator)

    await db.commit()
    await db.refresh(creator)
    return creator