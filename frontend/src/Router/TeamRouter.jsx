import React from "react";
import { AuthScreen } from "../components/AuthScreen";
import { DashboardMetrics } from "../components/DashboardMetrics";
import { Header } from "../components/Header";
import { ProjectsPanel } from "../components/ProjectsPanel";
import { TasksPanel } from "../components/TasksPanel";
import { TeamPanel } from "../components/TeamPanel";

function TeamRouter({
  assignableUsers,
  canCreateTasks,
  dashboard,
  handlers,
  isAdmin,
  memberForms,
  message,
  projectForm,
  projects,
  taskForm,
  tasks,
  user,
  users,
}) {
  if (!user) return <AuthScreen onAuth={handlers.setUser} />;

  return (
    <main className="app-shell">
      <Header isAdmin={isAdmin} user={user} onLogout={handlers.logout} />
      <DashboardMetrics dashboard={dashboard} />
      {message && <p className="error">{message}</p>}

      <section className={`workspace-grid ${isAdmin ? "admin-grid" : ""}`}>
        {isAdmin && (
          <TeamPanel
            currentUser={user}
            users={users}
            onDeleteUser={handlers.deleteUser}
            onUpdateRole={handlers.updateRole}
          />
        )}
        <ProjectsPanel
          isAdmin={isAdmin}
          memberForms={memberForms}
          onAddProjectMember={handlers.addProjectMember}
          onCreateProject={handlers.createProject}
          onDeleteProject={handlers.deleteProject}
          onProjectFormChange={handlers.setProjectForm}
          onRemoveProjectMember={handlers.removeProjectMember}
          onSetMemberForms={handlers.setMemberForms}
          projectForm={projectForm}
          projects={projects}
          users={users}
        />
        <TasksPanel
          assignableUsers={assignableUsers}
          canCreateTasks={canCreateTasks}
          onCreateTask={handlers.createTask}
          onTaskFormChange={handlers.setTaskForm}
          onUpdateStatus={handlers.updateStatus}
          projects={projects}
          taskForm={taskForm}
          tasks={tasks}
        />
      </section>
    </main>
  );
}

export default TeamRouter;
