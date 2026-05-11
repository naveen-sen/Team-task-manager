from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.project_member_model import ProjectMember
from ..models.task_model import Task
from ..models.user_model import User
from ..schemas import schemas
from .project_services import ensure_project_access, ensure_project_manager, get_project_with_members, serialize_project


def add_member(db: Session, project_id: int, payload: schemas.MemberUpdate, current_user: User) -> schemas.ProjectOut:
    project = ensure_project_access(db, project_id, current_user)
    ensure_project_manager(project, current_user)
    if not db.get(User, payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    exists = db.query(ProjectMember).filter_by(project_id=project_id, user_id=payload.user_id).first()
    if not exists:
        db.add(ProjectMember(project_id=project_id, user_id=payload.user_id))
        db.commit()
    return serialize_project(get_project_with_members(db, project_id))


def remove_member(db: Session, project_id: int, user_id: int, current_user: User) -> schemas.ProjectOut:
    project = ensure_project_access(db, project_id, current_user)
    ensure_project_manager(project, current_user)
    if project.owner_id == user_id:
        raise HTTPException(status_code=400, detail="Project owner cannot be removed from their project")

    membership = db.query(ProjectMember).filter_by(project_id=project_id, user_id=user_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Project member not found")

    db.query(Task).filter(
        Task.project_id == project_id,
        Task.assignee_id == user_id,
    ).update({Task.assignee_id: None}, synchronize_session=False)
    db.delete(membership)
    db.commit()
    return serialize_project(get_project_with_members(db, project_id))
