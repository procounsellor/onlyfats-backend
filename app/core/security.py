import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def normalize_email(email: str | None) -> str | None:
    if email is None:
        return None
    cleaned = email.strip().lower()
    return cleaned or None


def hash_password(password: str) -> str:
    if password is None or not password.strip():
        raise ValueError("Password is required")
    return password_hash.hash(password)


def verify_password(password: str | None, hashed_password: str | None) -> bool:
    if not password or not hashed_password:
        return False
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": subject,
        "type": "access",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> tuple[str, str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    jti = secrets.token_urlsafe(48)
    payload = {
        "sub": subject,
        "jti": jti,
        "type": "refresh",
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return token, token_hash, expires_at


def hash_token(token: str) -> str:
    if token is None or not token.strip():
        raise ValueError("Token is required")
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid access token") from exc


def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid refresh token") from exc