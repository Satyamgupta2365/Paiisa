import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database.db import Base, get_db
from database.models import Offer, PaymentMethod
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = async_sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    session = TestingSessionLocal()
    yield session
    
    await session.close()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def sample_offers():
    now = datetime.utcnow()
    return [
        Offer(payment_method=PaymentMethod.CREDIT_CARD, cashback_percentage=10.0, max_cashback=1000, min_amount=500, category="electronics", valid_until=now + timedelta(days=30), is_active=True),
        Offer(payment_method=PaymentMethod.UPI, cashback_percentage=3.0, max_cashback=150, min_amount=0, valid_until=now + timedelta(days=30), is_active=True),
        Offer(payment_method=PaymentMethod.WALLET, cashback_percentage=5.0, max_cashback=250, min_amount=0, valid_until=now + timedelta(days=30), is_active=True)
    ]
