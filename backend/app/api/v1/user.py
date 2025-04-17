from fastapi import APIRouter, Depends, HTTPException, status
from app.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService
from app.db.session import get_session
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    service = UserService(session)
    existing = await service.get_by_username(user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = await service.create_user(user_data)
    return user


@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(get_current_user)):
    return UserRead.model_validate(user)
