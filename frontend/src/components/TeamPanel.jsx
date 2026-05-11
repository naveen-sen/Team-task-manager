import React from "react";
import { Trash2 } from "lucide-react";

export function TeamPanel({ currentUser, users, onDeleteUser, onUpdateRole }) {
  return (
    <div className="panel">
      <h2>Team</h2>
      <div className="list">
        {users.map((member) => (
          <article className="card member-card" key={member.id}>
            <div>
              <h3>{member.name}</h3>
              <p>{member.email}</p>
            </div>
            <div className="row-actions">
              <select value={member.role} onChange={(e) => onUpdateRole(member, e.target.value)} disabled={member.id === currentUser.id}>
                <option>Member</option>
                <option>Admin</option>
              </select>
              <button className="danger-icon" onClick={() => onDeleteUser(member)} disabled={member.id === currentUser.id} title="Delete user">
                <Trash2 size={16} />
              </button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
