from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import select

from app.core.config import settings

# Create async engine according to SQLAlchemy 2.0 conventions
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Add method to get a model by primary key
async def get_by_id(session, model, id):
    """Get a model instance by ID."""
    stmt = select(model).where(model.id == id)
    result = await session.execute(stmt)
    return result.scalars().first()

# Add the get method to AsyncSession
AsyncSession.get = get_by_id


# Dependency to get DB session
async def get_db() -> AsyncSession:
    """
    Dependency that provides a database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Utility function to get a test database session
def get_test_db_url() -> str:
    """
    Get the test database URL from settings
    """
    return str(settings.TEST_DATABASE_URL or settings.DATABASE_URL)


# Create test engine
def create_test_engine():
    """
    Create a test engine with NullPool to avoid connection leaks
    """
    test_url = get_test_db_url()
    return create_async_engine(
        test_url,
        echo=False,
        pool_pre_ping=True,
        poolclass=NullPool,
        future=True,
    ) 