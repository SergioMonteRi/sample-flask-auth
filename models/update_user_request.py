from pydantic import BaseModel, Field


class UpdateUserRequest(BaseModel):
    password: str = Field(max_length=30, min_length=8)