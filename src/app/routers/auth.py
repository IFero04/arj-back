from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.session import create_session
from const import (
    AUTH_TAGS,
    AUTH_URL,
)
from schemas.auth import (
    TokenSchema,
    UserSchema,
    CreateUserSchema
)
from services.auth import AuthService


router = APIRouter(prefix="/" + AUTH_URL, tags=AUTH_TAGS)


@router.post("", response_model=TokenSchema)
async def authenticate(
    login: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(create_session),
) -> TokenSchema | None:
    return AuthService(session).authenticate(login)

@router.post("/register", response_model=UserSchema)
async def register_user(
    user: CreateUserSchema,
    session: Session = Depends(create_session),
) -> UserSchema:
    try:
        auth_service = AuthService(session)
        auth_service.create_user(user)
        return UserSchema(name=user.name, email=user.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        