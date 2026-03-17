from pydantic import BaseModel, Field
from typing import Optional, List


class CreatePostRequest(BaseModel):
    caption: Optional[str] = None
    visibility: str = Field(..., pattern="^(public|subscribers_only)$")
    media_type: str = Field(..., pattern="^(image|video|mixed)$")


class AddPostMediaRequest(BaseModel):
    media_kind: str = Field(..., pattern="^(photo|video)$")
    bucket_name: str
    object_path: str
    thumbnail_object_path: Optional[str] = None
    mime_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    duration_seconds: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int = 0
    processing_status: str = "ready"


class PublishPostRequest(BaseModel):
    pass


class PostMediaResponse(BaseModel):
    id: int
    media_kind: str
    bucket_name: str
    object_path: str
    thumbnail_object_path: Optional[str] = None
    mime_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    duration_seconds: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int
    processing_status: str

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    post_id: int
    creator_id: int
    caption: Optional[str]
    visibility: str
    media_type: str
    status: str
    moderation_status: str
    like_count: int
    comment_count: int
    published_at: Optional[str]
    created_at: Optional[str]
    media: List[PostMediaResponse]


class FeedItemResponse(BaseModel):
    post_id: int
    creator_id: int
    creator_display_name: Optional[str]
    caption: Optional[str]
    visibility: str
    media_type: str
    like_count: int
    comment_count: int
    has_access: bool
    locked: bool
    created_at: Optional[str]
    media: List[PostMediaResponse]