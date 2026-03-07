import React from "react";

import type { RecordDetail } from "../lib/placeholder-records";

export default function RecordDetailPanel({
  moduleLabel,
  detailLabel,
  item,
  emptyLabel,
}: {
  moduleLabel: string;
  detailLabel: string;
  item: RecordDetail | undefined;
  emptyLabel: string;
}) {
  if (!item) {
    return (
      <main>
        <section className="section panel">
          <h3>{emptyLabel}</h3>
        </section>
      </main>
    );
  }

  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">{moduleLabel}</span>
        <h2>{detailLabel}</h2>
        <p>{item.record_no}</p>
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