from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.db.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, data: UserCreate) -> User:
        hashed = self.hash_password(data.password)
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hashed,
            role=data.role,
        )
        return await self.repo.create(user)

    async def get_by_username(self, username: str) -> User | None:
        return await self.repo.get_by_username(username)
