from sqlalchemy.ext.asyncio import AsyncSession
from app.user.services import UserService
from app.user.models import User
from app.core.security import verify_password


class AuthService:
    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
        user = await UserService.get_user_by_username(session, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
