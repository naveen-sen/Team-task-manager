import React from "react";

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export function DashboardMetrics({ dashboard }) {
  if (!dashboard) return null;

  return (
    <section className="metrics-grid">
      <Metric label="Total tasks" value={dashboard.total_tasks} />
      <Metric label="In progress" value={dashboard.in_progress} />
      <Metric label="Done" value={dashboard.done} />
      <Metric label="Overdue" value={dashboard.overdue} />
      <Metric label="Assigned to me" value={dashboard.assigned_to_me} />
    </section>
  );
}
