import React from "react";
import { FolderKanban, LogOut, Shield } from "lucide-react";

export function Header({ isAdmin, user, onLogout }) {
  return (
    <header className="topbar">
      <div className="brand-row">
        <FolderKanban />
        <span>Team Task Manager</span>
      </div>
      <div className="user-chip">
        {isAdmin && <Shield size={16} />}
        <span>{user.name} - {user.role}</span>
        <button className="icon-button" onClick={onLogout} title="Logout">
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
}
