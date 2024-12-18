import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, init_db, SessionLocal
from main import app  # Import your FastAPI app

# Use the test database from .env
from database.database import DATABASE_URL

# Test database setup
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[SessionLocal] = override_get_db

# Set up database schema
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test client fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
