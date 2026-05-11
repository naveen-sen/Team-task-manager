# Team Task Manager

A full-stack team task manager with FastAPI, SQLite, SQLAlchemy, JWT authentication, role-based access control, and a React dashboard.

## Features

- Signup and login with JWT auth
- Admin and Member roles
- Project creation and member assignment
- Admin team view for role changes
- Task creation, assignment, status updates, and due dates
- Dashboard metrics for total, in-progress, done, overdue, and assigned tasks
- Relational database models for users, projects, project members, and tasks

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

## Notes

- The first registered user is automatically promoted to `Admin`.
- Admins can create projects and list all users.
- Later signups are created as `Member`; Admins can promote users from the Team panel.
- Admins and project owners can create and assign tasks.
- Members can see accessible projects and update the status of tasks assigned to them.
