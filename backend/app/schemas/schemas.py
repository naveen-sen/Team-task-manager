from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from ..models.user_model import Role
from ..models.task_model import TaskStatus


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserOut(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=140)
    description: str | None = Field(default=None, max_length=1000)
    member_ids: list[int] = []


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    members: list[UserOut] = []

    class Config:
        from_attributes = True


class MemberUpdate(BaseModel):
    user_id: int


class RoleUpdate(BaseModel):
    role: Role


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    description: str | None = Field(default=None, max_length=2000)
    project_id: int
    assignee_id: int | None = None
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: datetime | None
    project_id: int
    assignee_id: int | None
    creator_id: int
    created_at: datetime
    assignee: UserOut | None = None

    class Config:
        from_attributes = True


class DashboardOut(BaseModel):
    total_tasks: int
    todo: int
    in_progress: int
    done: int
    overdue: int
    assigned_to_me: int
