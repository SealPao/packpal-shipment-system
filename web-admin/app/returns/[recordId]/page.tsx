import React from "react";

import { recordData } from "../../../lib/placeholder-records";

export default function ReturnDetailPage({
  params,
}: {
  params: { recordId: string };
}) {
  const item = recordData.returns.find((entry) => entry.id === params.recordId);

  if (!item) {
    return <main><section className="section panel"><h3>Return not found</h3></section></main>;
  }

  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Return Detail</span>
        <h2>{item.record_no}</h2>
        <p>{item.notes}</p>
      </section>

      <section className="section panel">
        <h3>Attachments</h3>
        <ul className="placeholder-list">
          {item.attachments.map((attachment) => (
            <li key={attachment}>{attachment}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}