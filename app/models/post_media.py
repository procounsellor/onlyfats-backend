from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class PostMedia(Base):
    __tablename__ = "post_media"

    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)

    media_kind = Column(String(20), nullable=False)  # photo, video
    storage_provider = Column(String(20), nullable=False, default="gcs")
    bucket_name = Column(String(255), nullable=False)
    object_path = Column(Text, nullable=False)
    thumbnail_object_path = Column(Text, nullable=True)

    mime_type = Column(String(100), nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    sort_order = Column(Integer, nullable=False, default=0)
    processing_status = Column(String(30), nullable=False, default="ready")

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    post = relationship("Post", back_populates="media_items")