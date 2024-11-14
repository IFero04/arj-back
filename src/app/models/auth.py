from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from models.base import SQLModel


class UserModel(SQLModel):
    __tablename__ = "users"
    __table_args__ = {"schema": "myapi"}

    email: Mapped[str] = mapped_column("email", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    hashed_password: Mapped[str] = mapped_column("hashed_password")