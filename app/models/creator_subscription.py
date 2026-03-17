from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base


class CreatorSubscription(Base):
    __tablename__ = "creator_subscriptions"

    id = Column(BigInteger, primary_key=True, index=True)
    subscriber_user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    creator_id = Column(BigInteger, ForeignKey("creators.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(String(30), nullable=False)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())