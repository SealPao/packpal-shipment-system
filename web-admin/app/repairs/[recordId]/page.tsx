import React from "react";

import { recordData } from "../../../lib/placeholder-records";

export default function RepairDetailPage({
  params,
}: {
  params: { recordId: string };
}) {
  const item = recordData.repairs.find((entry) => entry.id === params.recordId);

  if (!item) {
    return <main><section className="section panel"><h3>Repair not found</h3></section></main>;
  }

  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Repair Detail</span>
        <h2>{item.record_no}</h2>
        <p>{item.notes}</p>
      </section>

      <section className="section panel">
        <h3>Tags</h3>
        <ul className="placeholder-list">
          {item.tags.map((tag) => (
            <li key={tag}>{tag}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}