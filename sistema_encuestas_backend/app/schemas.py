from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None


class SurveyCreate(SurveyBase):
    pass


class Survey(SurveyBase):
    id: UUID
    creator_id: Optional[UUID] = None

    class Config:
        orm_mode = True
