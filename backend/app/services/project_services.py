from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from ..models.project_member_model import ProjectMember
from ..models.project_model import Project
from ..models.user_model import Role, User
from ..schemas import schemas


def ensure_project_access(db: Session, project_id: int, user: User) -> Project:
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if user.role == Role.ADMIN:
        return project
    is_member = any(member.user_id == user.id for member in project.members)
    if project.owner_id != user.id and not is_member:
        raise HTTPException(status_code=403, detail="Project access denied")
    return project


def ensure_project_manager(project: Project, user: User) -> None:
    if user.role == Role.ADMIN or project.owner_id == user.id:
        return
    raise HTTPException(status_code=403, detail="Only admins or project owners can manage this resource")


def serialize_project(project: Project) -> schemas.ProjectOut:
    users = [member.user for member in project.members]
    return schemas.ProjectOut(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        created_at=project.created_at,
        members=users,
    )


def get_project_with_members(db: Session, project_id: int) -> Project | None:
    return (
        db.query(Project)
        .options(joinedload(Project.members).joinedload(ProjectMember.user))
        .filter(Project.id == project_id)
        .first()
    )


def create_project(db: Session, payload: schemas.ProjectCreate, current_user: User) -> schemas.ProjectOut:
    project = Project(name=payload.name, description=payload.description, owner_id=current_user.id)
    db.add(project)
    db.flush()
    db.add(ProjectMember(project_id=project.id, user_id=current_user.id))
    for user_id in set(payload.member_ids) - {current_user.id}:
        if not db.get(User, user_id):
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        db.add(ProjectMember(project_id=project.id, user_id=user_id))
    db.commit()
    return serialize_project(get_project_with_members(db, project.id))


def list_projects(db: Session, current_user: User) -> list[schemas.ProjectOut]:
    query = db.query(Project).options(joinedload(Project.members).joinedload(ProjectMember.user))
    if current_user.role != Role.ADMIN:
        query = query.join(ProjectMember).filter(ProjectMember.user_id == current_user.id)
    return [serialize_project(project) for project in query.order_by(Project.created_at.desc()).all()]


def delete_project(db: Session, project_id: int, current_user: User) -> None:
    project = ensure_project_access(db, project_id, current_user)
    ensure_project_manager(project, current_user)
    db.delete(project)
    db.commit()
