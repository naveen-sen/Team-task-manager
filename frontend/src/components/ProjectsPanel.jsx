import React from "react";
import { Plus, Trash2, UserMinus, UserPlus } from "lucide-react";

export function ProjectsPanel({
  isAdmin,
  memberForms,
  onAddProjectMember,
  onCreateProject,
  onDeleteProject,
  onProjectFormChange,
  onRemoveProjectMember,
  onSetMemberForms,
  projectForm,
  projects,
  users,
}) {
  return (
    <div className="panel">
      <h2>Projects</h2>
      {isAdmin && (
        <form onSubmit={onCreateProject} className="stack">
          <input placeholder="Project name" value={projectForm.name} onChange={(e) => onProjectFormChange({ ...projectForm, name: e.target.value })} required />
          <textarea placeholder="Description" value={projectForm.description} onChange={(e) => onProjectFormChange({ ...projectForm, description: e.target.value })} />
          <select
            multiple
            value={projectForm.member_ids.map(String)}
            onChange={(e) => onProjectFormChange({ ...projectForm, member_ids: Array.from(e.target.selectedOptions, (option) => Number(option.value)) })}
          >
            {users.map((member) => <option key={member.id} value={member.id}>{member.name}</option>)}
          </select>
          <button className="primary" type="submit"><Plus size={16} /> Project</button>
        </form>
      )}

      <div className="list">
        {projects.map((project) => (
          <article className="card" key={project.id}>
            <div className="card-header">
              <h3>{project.name}</h3>
              {isAdmin && (
                <button className="danger-icon" onClick={() => onDeleteProject(project)} title="Delete project">
                  <Trash2 size={16} />
                </button>
              )}
            </div>
            <p>{project.description || "No description"}</p>
            <div className="member-list">
              {project.members.map((member) => (
                <span className="member-pill" key={member.id}>
                  {member.name}
                  {isAdmin && member.id !== project.owner_id && (
                    <button onClick={() => onRemoveProjectMember(project, member)} title="Remove member">
                      <UserMinus size={14} />
                    </button>
                  )}
                </span>
              ))}
            </div>
            {isAdmin && (
              <div className="inline-form">
                <select value={memberForms[project.id] || ""} onChange={(e) => onSetMemberForms({ ...memberForms, [project.id]: e.target.value })}>
                  <option value="">Add member</option>
                  {users
                    .filter((member) => !project.members.some((projectMember) => projectMember.id === member.id))
                    .map((member) => <option key={member.id} value={member.id}>{member.name}</option>)}
                </select>
                <button className="icon-button" onClick={() => onAddProjectMember(project)} title="Add member">
                  <UserPlus size={16} />
                </button>
              </div>
            )}
          </article>
        ))}
      </div>
    </div>
  );
}
