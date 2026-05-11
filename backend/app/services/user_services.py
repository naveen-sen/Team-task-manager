from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..Auth import auth
from ..models.project_member_model import ProjectMember
from ..models.project_model import Project
from ..models.task_model import Task
from ..models.user_model import Role, User
from ..schemas import schemas


def signup(db: Session, payload: schemas.UserCreate) -> schemas.Token:
    existing = db.query(User).filter(func.lower(User.email) == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email is already registered")

    user_count = db.query(User).count()
    role = Role.ADMIN if user_count == 0 else Role.MEMBER
    user = User(
        name=payload.name,
        email=payload.email.lower(),
        password_hash=auth.hash_password(payload.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.Token(access_token=auth.create_access_token(user.id), user=user)


def login(db: Session, payload: schemas.LoginRequest) -> schemas.Token:
    user = db.query(User).filter(func.lower(User.email) == payload.email.lower()).first()
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return schemas.Token(access_token=auth.create_access_token(user.id), user=user)


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.name).all()


def update_user_role(db: Session, user_id: int, payload: schemas.RoleUpdate, current_user: User) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id and payload.role != Role.ADMIN:
        raise HTTPException(status_code=400, detail="You cannot remove your own admin role")
    user.role = payload.role
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int, current_user: User) -> None:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    owned_projects = db.query(Project).filter(Project.owner_id == user.id).all()
    for project in owned_projects:
        db.delete(project)

    db.query(Task).filter(Task.assignee_id == user.id).update(
        {Task.assignee_id: None},
        synchronize_session=False,
    )
    db.query(Task).filter(Task.creator_id == user.id).update(
        {Task.creator_id: current_user.id},
        synchronize_session=False,
    )
    db.query(ProjectMember).filter(ProjectMember.user_id == user.id).delete(synchronize_session=False)
    db.delete(user)
    db.commit()
