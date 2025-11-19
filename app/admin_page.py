import secrets
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings
from app.user.admin import register_user_views


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        # Constant-time comparison for superuser
        is_username_ok = secrets.compare_digest(username, settings.FIRST_SUPERUSER)
        is_password_ok = secrets.compare_digest(password, settings.FIRST_SUPERUSER_PASSWORD)

        if not (is_username_ok and is_password_ok):
            return False

        request.session.update({"is_admin": True})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("is_admin") is True


def setup_admin(app, engine):
    auth_backend = AdminAuth(secret_key=settings.SECRET_KEY)

    admin = Admin(
        app,
        engine,
        authentication_backend=auth_backend,
        title=f"{settings.PROJECT_NAME} Admin"
    )
    register_user_views(admin)
    return admin
