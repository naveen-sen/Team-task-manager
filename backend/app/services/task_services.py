from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from ..models.project_member_model import ProjectMember
from ..models.task_model import Task, TaskStatus
from ..models.user_model import Role, User
from ..schemas import schemas
from .project_services import ensure_project_access, ensure_project_manager


def create_task(db: Session, payload: schemas.TaskCreate, current_user: User) -> Task:
    project = ensure_project_access(db, payload.project_id, current_user)
    ensure_project_manager(project, current_user)
    if payload.assignee_id:
        ensure_project_access(db, payload.project_id, db.get(User, payload.assignee_id))
    task = Task(**payload.model_dump(), creator_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, current_user: User) -> list[Task]:
    query = db.query(Task).options(joinedload(Task.assignee))
    if current_user.role != Role.ADMIN:
        project_ids = db.query(ProjectMember.project_id).filter(ProjectMember.user_id == current_user.id)
        query = query.filter(or_(Task.assignee_id == current_user.id, Task.project_id.in_(project_ids)))
    return query.order_by(Task.created_at.desc()).all()


def update_task(db: Session, task_id: int, payload: schemas.TaskUpdate, current_user: User) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    project = ensure_project_access(db, task.project_id, current_user)
    can_manage = current_user.role == Role.ADMIN or project.owner_id == current_user.id
    if not can_manage and task.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Task access denied")

    updates = payload.model_dump(exclude_unset=True)
    if not can_manage:
        updates = {"status": updates["status"]} if "status" in updates else {}
    if "assignee_id" in updates and updates["assignee_id"]:
        ensure_project_access(db, task.project_id, db.get(User, updates["assignee_id"]))
    for field, value in updates.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def dashboard(db: Session, current_user: User) -> schemas.DashboardOut:
    tasks = list_tasks(db, current_user)
    now = datetime.utcnow()
    return schemas.DashboardOut(
        total_tasks=len(tasks),
        todo=sum(task.status == TaskStatus.TODO for task in tasks),
        in_progress=sum(task.status == TaskStatus.IN_PROGRESS for task in tasks),
        done=sum(task.status == TaskStatus.DONE for task in tasks),
        overdue=sum(bool(task.due_date and task.due_date < now and task.status != TaskStatus.DONE) for task in tasks),
        assigned_to_me=sum(task.assignee_id == current_user.id for task in tasks),
    )
