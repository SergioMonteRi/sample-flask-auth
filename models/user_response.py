from uuid import UUID
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: str