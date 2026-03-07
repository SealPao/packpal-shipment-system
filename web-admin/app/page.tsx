import React from "react";
import Link from "next/link";

const modules = [
  {
    title: "Shipment Workspace",
    href: "/shipments",
    description: "Placeholder for shipment processing summaries and queue status.",
  },
  {
    title: "Repair Intake",
    href: "/repairs",
    description: "Placeholder for repair receiving records and pending verification.",
  },
  {
    title: "Return Intake",
    href: "/returns",
    description: "Placeholder for return receiving records and issue classification.",
  },
];

export default function DashboardPage() {
  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">v0.1.0 skeleton</span>
        <h2>Operational overview</h2>
        <p>
          This dashboard is intentionally minimal. It establishes the admin
          layout, navigation, and presentation structure that later pages can
          extend once the API and search workflows are ready.
        </p>
      </section>

      <section className="grid">
        {modules.map((item) => (
          <article className="card panel" key={item.title}>
            <h3>{item.title}</h3>
            <p>{item.description}</p>
            <p>
              <Link href={item.href}>Open module</Link>
            </p>
          </article>
        ))}
      </section>

      <section className="section panel">
        <h3>Next integration points</h3>
        <ul className="placeholder-list">
          <li>Authentication and role-based access</li>
          <li>Record search, filtering, and detail drill-down</li>
          <li>Media preview for snapshots, videos, and documents</li>
        </ul>
      </section>
    </main>
  );
}