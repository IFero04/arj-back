from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy import select

from backend.config import config
from const import (
    AUTH_URL,
    TOKEN_ALGORITHM,
    TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
)
from exc import raise_with_log
from models.auth import UserModel
from schemas.auth import (
    CreateUserSchema,
    TokenSchema,
    UserSchema,
)
from services.base import (
    BaseDataManager,
    BaseService,
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL, auto_error=False)


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    if token is None:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    try:
        payload = jwt.decode(token, config.token_key, algorithms=[TOKEN_ALGORITHM])

        name: str = payload.get("name")
        sub: str = payload.get("sub")
        expires_at: str = payload.get("expires_at")

        if sub is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return UserSchema(name=name, email=sub)
    except PyJWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    return None


def is_expired(expires_at: str) -> bool:
    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.utcnow()


class HashingMixin:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class AuthService(HashingMixin, BaseService):
    def create_user(self, user: CreateUserSchema) -> None:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=self.bcrypt(user.password),
        )

        AuthDataManager(self.session).add_user(user_model)

    def authenticate(
        self, login: OAuth2PasswordRequestForm = Depends()
    ) -> TokenSchema | None:
        user = AuthDataManager(self.session).get_user(login.username)

        if user.hashed_password is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
        else:
            if not self.verify(user.hashed_password, login.password):
                raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
            else:
                access_token = self._create_access_token(user.name, user.email)
                return TokenSchema(access_token=access_token, token_type=TOKEN_TYPE)
        return None

    def _create_access_token(self, name: str, email: str) -> str:
        payload = {
            "name": name,
            "sub": email,
            "expires_at": self._expiration_time(),
        }

        return jwt.encode(payload, config.token_key, algorithm=TOKEN_ALGORITHM)

    @staticmethod
    def _expiration_time() -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")


class AuthDataManager(BaseDataManager):
    def add_user(self, user: UserModel) -> None:
        self.add_one(user)

    def get_user(self, email: str) -> UserSchema:
        model = self.get_one(select(UserModel).where(UserModel.email == email))

        if not isinstance(model, UserModel):
            raise_with_log(status.HTTP_404_NOT_FOUND, "User not found")

        return UserSchema(
            name=model.name,
            email=model.email,
            hashed_password=model.hashed_password,
        )