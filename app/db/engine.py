from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine
# echo=True prints SQL queries to console (good for debugging, turn off in production)
# pool_pre_ping=True ensures the connection is alive before using it
engine = create_async_engine(
    str(settings.ASYNC_SQLALCHEMY_DATABASE_URI),
    # echo=False,
    future=True,
    pool_pre_ping=True
)

# Create async session maker
async_session_maker: AsyncSession = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
