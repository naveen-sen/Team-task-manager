from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..Auth import auth
from ..db.database import get_db
from ..models.user_model import User
from ..schemas import schemas
from ..services import user_services

user_router = APIRouter(prefix="/api", tags=["Users"])


@user_router.post("/auth/signup", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_services.signup(db, payload)


@user_router.post("/auth/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    return user_services.login(db, payload)


@user_router.get("/users", response_model=list[schemas.UserOut])
def list_users(_: User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    return user_services.list_users(db)


@user_router.patch("/users/{user_id}/role", response_model=schemas.UserOut)
def update_user_role(
    user_id: int,
    payload: schemas.RoleUpdate,
    current_user: User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    return user_services.update_user_role(db, user_id, payload, current_user)


@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(auth.require_admin),
    db: Session = Depends(get_db),
):
    user_services.delete_user(db, user_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.get("/me", response_model=schemas.UserOut)
def me(current_user: User = Depends(auth.get_current_user)):
    return current_user
