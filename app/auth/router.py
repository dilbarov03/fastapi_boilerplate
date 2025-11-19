from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.schemas import UserCreate, UserLogin, UserRead, Token
from app.user.models import User
from app.user.services import UserService
from app.auth.services import AuthService
from app.core.security import create_access_token
from app.core.config import settings
from app.api.dependency import get_current_active_user, get_db

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_db)
):
    if await UserService.get_user_by_username(session, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    if await UserService.get_user_by_email(session, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await UserService.create_user(session, user_data)
    return {"message": "User created successfully", "user_id": user.id}


@router.post("/login", response_model=Token)
async def login(
        login_data: UserLogin,
        session: AsyncSession = Depends(get_db)
):
    user = await AuthService.authenticate_user(session, login_data.username, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
):
    return current_user
