from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..Auth import auth
from ..db.database import get_db
from ..models.user_model import User
from ..schemas import schemas
from ..services import project_services

project_router = APIRouter(prefix="/api", tags=["Projects"])


@project_router.post("/projects", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: schemas.ProjectCreate,
    current_user: User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    return project_services.create_project(db, payload, current_user)


@project_router.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return project_services.list_projects(db, current_user)


@project_router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    project_services.delete_project(db, project_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
