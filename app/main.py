from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.core.config import settings
from app.api.router import api_router
from app.admin_page import setup_admin
from app.db.engine import engine as async_engine


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_pagination(app)

    app.include_router(api_router, prefix="/api")
    setup_admin(app, async_engine)
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "FastAPI Boilerplate API"}
