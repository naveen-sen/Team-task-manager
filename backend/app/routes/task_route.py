from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..Auth import auth
from ..db.database import get_db
from ..models.user_model import User
from ..schemas import schemas
from ..services import task_services

task_router = APIRouter(prefix="/api", tags=["Tasks"])


@task_router.post("/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: schemas.TaskCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return task_services.create_task(db, payload, current_user)


@task_router.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return task_services.list_tasks(db, current_user)


@task_router.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return task_services.update_task(db, task_id, payload, current_user)


@task_router.get("/dashboard", response_model=schemas.DashboardOut)
def dashboard(current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return task_services.dashboard(db, current_user)
