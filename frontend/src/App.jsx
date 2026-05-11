import React, { useEffect, useMemo, useState } from "react";
import { api } from "./api";
import TeamRouter from "./Router/TeamRouter";

const emptyProjectForm = { name: "", description: "", member_ids: [] };
const emptyTaskForm = { title: "", description: "", project_id: "", assignee_id: "", due_date: "" };

export default function App() {
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");
  const [projectForm, setProjectForm] = useState(emptyProjectForm);
  const [taskForm, setTaskForm] = useState(emptyTaskForm);
  const [memberForms, setMemberForms] = useState({});

  const isAdmin = user?.role === "Admin";
  const visibleUsers = useMemo(() => {
    if (users.length) return users;
    const memberMap = new Map();
    projects.forEach((project) => project.members.forEach((member) => memberMap.set(member.id, member)));
    if (user) memberMap.set(user.id, user);
    return Array.from(memberMap.values());
  }, [projects, users, user]);
  const selectedProject = useMemo(
    () => projects.find((project) => String(project.id) === String(taskForm.project_id)),
    [projects, taskForm.project_id],
  );
  const assignableUsers = selectedProject?.members?.length ? selectedProject.members : visibleUsers;
  const canCreateTasks = Boolean(user) && (isAdmin || projects.some((project) => project.owner_id === user.id));

  async function loadAll() {
    const [dash, projectList, taskList] = await Promise.all([api("/dashboard"), api("/projects"), api("/tasks")]);
    setDashboard(dash);
    setProjects(projectList);
    setTasks(taskList);
    if (isAdmin) setUsers(await api("/users"));
  }

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;
    api("/me").then(setUser).catch(() => localStorage.removeItem("token"));
  }, []);

  useEffect(() => {
    if (user) loadAll().catch((err) => setMessage(err.message));
  }, [user]);

  async function createProject(event) {
    event.preventDefault();
    try {
      await api("/projects", { method: "POST", body: JSON.stringify(projectForm) });
      setProjectForm(emptyProjectForm);
      await loadAll();
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function createTask(event) {
    event.preventDefault();
    const payload = {
      ...taskForm,
      project_id: Number(taskForm.project_id),
      assignee_id: taskForm.assignee_id ? Number(taskForm.assignee_id) : null,
      due_date: taskForm.due_date ? new Date(taskForm.due_date).toISOString() : null,
    };
    try {
      await api("/tasks", { method: "POST", body: JSON.stringify(payload) });
      setTaskForm(emptyTaskForm);
      await loadAll();
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function updateStatus(task, status) {
    await api(`/tasks/${task.id}`, { method: "PATCH", body: JSON.stringify({ status }) });
    await loadAll();
  }

  async function updateRole(member, role) {
    await api(`/users/${member.id}/role`, { method: "PATCH", body: JSON.stringify({ role }) });
    await loadAll();
  }

  async function deleteUser(member) {
    if (!confirm(`Delete ${member.name} from the team?`)) return;
    await api(`/users/${member.id}`, { method: "DELETE" });
    await loadAll();
  }

  async function deleteProject(project) {
    if (!confirm(`Delete project "${project.name}" and all its tasks?`)) return;
    await api(`/projects/${project.id}`, { method: "DELETE" });
    await loadAll();
  }

  async function addProjectMember(project) {
    const userId = Number(memberForms[project.id]);
    if (!userId) return;
    await api(`/projects/${project.id}/members`, { method: "POST", body: JSON.stringify({ user_id: userId }) });
    setMemberForms({ ...memberForms, [project.id]: "" });
    await loadAll();
  }

  async function removeProjectMember(project, member) {
    await api(`/projects/${project.id}/members/${member.id}`, { method: "DELETE" });
    await loadAll();
  }

  function logout() {
    localStorage.removeItem("token");
    setUser(null);
  }

  return (
    <TeamRouter
      assignableUsers={assignableUsers}
      canCreateTasks={canCreateTasks}
      dashboard={dashboard}
      handlers={{
        addProjectMember,
        createProject,
        createTask,
        deleteProject,
        deleteUser,
        logout,
        removeProjectMember,
        setMemberForms,
        setProjectForm,
        setTaskForm,
        setUser,
        updateRole,
        updateStatus,
      }}
      isAdmin={isAdmin}
      memberForms={memberForms}
      message={message}
      projectForm={projectForm}
      projects={projects}
      taskForm={taskForm}
      tasks={tasks}
      user={user}
      users={users}
    />
  );
}
