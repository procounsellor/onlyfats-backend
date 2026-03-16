from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    GuestLoginRequest,
    LoginRequest,
    RefreshRequest,
    SignupRequest,
    TokenResponse,
)
from app.schemas.user import MeResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
async def signup(
    payload: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.signup(db, payload)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.login(db, payload)


@router.post("/guest", response_model=TokenResponse)
async def guest_login(
    payload: GuestLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.guest_login(db, payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.refresh(db, payload)


@router.post("/logout")
async def logout(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.logout(db, payload)


@router.get("/me", response_model=MeResponse)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user