import React from "react";
import { Plus } from "lucide-react";

const statuses = ["Todo", "In Progress", "Done"];

export function TasksPanel({
  assignableUsers,
  canCreateTasks,
  onCreateTask,
  onTaskFormChange,
  onUpdateStatus,
  projects,
  taskForm,
  tasks,
}) {
  return (
    <div className="panel wide">
      <h2>Tasks</h2>
      {canCreateTasks && (
        <form onSubmit={onCreateTask} className="task-form">
          <input placeholder="Task title" value={taskForm.title} onChange={(e) => onTaskFormChange({ ...taskForm, title: e.target.value })} required />
          <select value={taskForm.project_id} onChange={(e) => onTaskFormChange({ ...taskForm, project_id: e.target.value, assignee_id: "" })} required>
            <option value="">Project</option>
            {projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}
          </select>
          <select value={taskForm.assignee_id} onChange={(e) => onTaskFormChange({ ...taskForm, assignee_id: e.target.value })}>
            <option value="">Unassigned</option>
            {assignableUsers.map((member) => <option key={member.id} value={member.id}>{member.name}</option>)}
          </select>
          <input type="date" value={taskForm.due_date} onChange={(e) => onTaskFormChange({ ...taskForm, due_date: e.target.value })} />
          <textarea placeholder="Description" value={taskForm.description} onChange={(e) => onTaskFormChange({ ...taskForm, description: e.target.value })} />
          <button className="primary" type="submit"><Plus size={16} /> Task</button>
        </form>
      )}

      <div className="task-board">
        {statuses.map((status) => (
          <section className="column" key={status}>
            <h3>{status}</h3>
            {tasks.filter((task) => task.status === status).map((task) => (
              <article className="card task-card" key={task.id}>
                <div>
                  <h4>{task.title}</h4>
                  <p>{task.description || "No description"}</p>
                </div>
                <small>{task.assignee?.name || "Unassigned"} {task.due_date ? `- due ${new Date(task.due_date).toLocaleDateString()}` : ""}</small>
                <select value={task.status} onChange={(e) => onUpdateStatus(task, e.target.value)}>
                  {statuses.map((item) => <option key={item}>{item}</option>)}
                </select>
              </article>
            ))}
          </section>
        ))}
      </div>
    </div>
  );
}
