import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import jwt
from datetime import datetime, timedelta

from ..app.database import Base, get_db
from .. import main
from ..app.models import User, UserRole, UserStatus
from ..app.routers.auth import SECRET_KEY, ALGORITHM

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with the test database."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    main.app.dependency_overrides[get_db] = override_get_db
    with TestClient(main.app) as client:
        yield client
    main.app.dependency_overrides = {}


@pytest.fixture(scope="function")
def tenant_user(db):
    """Create a tenant user for testing."""
    user = User(
        email="tenant@example.com",
        hashed_password="$2b$12$HxjEkIgt9.Y/xaRYbVw8XOTf1BNIYHzHLVO55zWKgcQZ6yvKpUzNW",  # password = 'Password123'
        full_name="Test Tenant",
        role=UserRole.TENANT,
        status=UserStatus.APPROVED,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def landlord_user(db):
    """Create a landlord user for testing."""
    user = User(
        email="landlord@example.com",
        hashed_password="$2b$12$HxjEkIgt9.Y/xaRYbVw8XOTf1BNIYHzHLVO55zWKgcQZ6yvKpUzNW",  # password = 'Password123'
        full_name="Test Landlord",
        role=UserRole.LANDLORD,
        status=UserStatus.APPROVED,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_user(db):
    """Create an admin user for testing."""
    user = User(
        email="admin@example.com",
        hashed_password="$2b$12$HxjEkIgt9.Y/xaRYbVw8XOTf1BNIYHzHLVO55zWKgcQZ6yvKpUzNW",  # password = 'Password123'
        full_name="Test Admin",
        role=UserRole.ADMIN,
        status=UserStatus.APPROVED,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_token(user_email):
    """Helper function to create a test JWT token."""
    access_token_expires = timedelta(minutes=30)
    expire = datetime.utcnow() + access_token_expires
    to_encode = {"sub": user_email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@pytest.fixture(scope="function")
def tenant_token(tenant_user):
    """Create a token for the tenant user."""
    return create_test_token(tenant_user.email)


@pytest.fixture(scope="function")
def landlord_token(landlord_user):
    """Create a token for the landlord user."""
    return create_test_token(landlord_user.email)


@pytest.fixture(scope="function")
def admin_token(admin_user):
    """Create a token for the admin user."""
    return create_test_token(admin_user.email) 