import React from "react";

export default function RecordsPage() {
  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Records</span>
        <h2>Records placeholder</h2>
        <p>
          This page will host shipment, repair, and return record search once
          the backend API contracts are finalized.
        </p>
      </section>

      <section className="section panel">
        <h3>Planned modules</h3>
        <ul className="placeholder-list">
          <li>Unified record table and filters</li>
          <li>Record detail side panel</li>
          <li>Attachment preview and audit timeline</li>
        </ul>
      </section>
    </main>
  );
}