import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_session

# Тестовая БД
TEST_DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/meeting_rooms_test"

engine_test = create_async_engine(TEST_DB_URL, future=True)
TestSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)

# Переопределение зависимостей
async def override_get_session() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture()
async def client() -> AsyncClient:
    async with TestSessionLocal() as session:
        # override на уровне этой одной общей сессии
        async def override_get_session() -> AsyncSession:
            yield session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c

# @pytest.fixture(autouse=True)
# async def clear_tables():
#     async with engine_test.begin() as conn:
#         for table in reversed(Base.metadata.sorted_tables):
#             await conn.execute(table.delete())
