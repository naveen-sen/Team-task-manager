from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.database import Base, engine
from .routes.project_route import project_router
from .routes.project_member_route import project_member_router
from .routes.task_route import task_router
from .routes.user_route import user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://team-task-manager-xi-umber.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)
app.include_router(project_member_router)
app.include_router(task_router)
app.include_router(user_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Team Task Manager API"}
