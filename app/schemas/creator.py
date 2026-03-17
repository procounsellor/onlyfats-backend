from pydantic import BaseModel, Field
from typing import Optional


class CreateOrUpdateCreatorProfileRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=150)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None


class CreatorProfileResponse(BaseModel):
    creator_id: int
    user_id: int
    display_name: Optional[str]
    bio: Optional[str]
    profile_image_url: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True