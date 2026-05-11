import React, { useState } from "react";
import { FolderKanban } from "lucide-react";
import { api } from "../api";

export function AuthScreen({ onAuth }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const endpoint = mode === "login" ? "/auth/login" : "/auth/signup";
      const payload = mode === "login" ? { email: form.email, password: form.password } : form;
      const result = await api(endpoint, { method: "POST", body: JSON.stringify(payload) });
      localStorage.setItem("token", result.access_token);
      onAuth(result.user);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="auth-layout">
      <section className="auth-panel">
        <div className="brand-row">
          <FolderKanban />
          <span>Team Task Manager</span>
        </div>
        <h1>{mode === "login" ? "Welcome back" : "Create your workspace account"}</h1>
        <form onSubmit={submit} className="stack">
          {mode === "signup" && (
            <input placeholder="Full name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          )}
          <input placeholder="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input placeholder="Password" type="password" minLength="8" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          {error && <p className="error">{error}</p>}
          <button className="primary" type="submit">{mode === "login" ? "Login" : "Sign up"}</button>
        </form>
        <button className="link-button" onClick={() => setMode(mode === "login" ? "signup" : "login")}>
          {mode === "login" ? "Need an account? Sign up" : "Already have an account? Login"}
        </button>
      </section>
    </main>
  );
}
