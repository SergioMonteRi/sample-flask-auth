from uuid import UUID, uuid7

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid7())
    )

    name: Mapped[str] = mapped_column(
        String(80), 
        nullable=False, 
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(30), 
        nullable=False
    )