import React from "react";
import Link from "next/link";

import type { RecordDetail } from "../lib/placeholder-records";

export default function RecordList({
  moduleLabel,
  modulePath,
  intro,
  items,
}: {
  moduleLabel: string;
  modulePath: string;
  intro: string;
  items: RecordDetail[];
}) {
  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">{moduleLabel}</span>
        <h2>{moduleLabel} module placeholder</h2>
        <p>{intro}</p>
      </section>

      <section className="grid">
        {items.map((item) => (
          <article className="card panel" key={item.id}>
            <h3>{item.record_no}</h3>
            <p>{item.customer_name}</p>
            <p>Status: {item.status}</p>
            <p>Updated: {item.updated_at}</p>
            <p>
              <Link href={`/${modulePath}/${item.id}`}>View detail</Link>
            </p>
          </article>
        ))}
      </section>
    </main>
  );
}