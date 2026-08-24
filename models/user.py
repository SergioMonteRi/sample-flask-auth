from uuid import UUID, uuid7

from sqlalchemy import String
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from custom_types.uuid import UUIDType

class User(Base, UserMixin):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        UUIDType(),
        primary_key=True,
        default=uuid7()
    )

    username: Mapped[str] = mapped_column(
        String(80), 
        nullable=False, 
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default="user"
    )