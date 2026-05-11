from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..Auth import auth
from ..db.database import get_db
from ..models.user_model import User
from ..schemas import schemas
from ..services import project_member_services

project_member_router = APIRouter(prefix="/api", tags=["Project Members"])


@project_member_router.post("/projects/{project_id}/members", response_model=schemas.ProjectOut)
def add_member(
    project_id: int,
    payload: schemas.MemberUpdate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return project_member_services.add_member(db, project_id, payload, current_user)


@project_member_router.delete("/projects/{project_id}/members/{user_id}", response_model=schemas.ProjectOut)
def remove_member(
    project_id: int,
    user_id: int,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return project_member_services.remove_member(db, project_id, user_id, current_user)
