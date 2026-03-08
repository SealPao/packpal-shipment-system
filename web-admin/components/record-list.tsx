import React from "react";
import Link from "next/link";

import type { RecordDetail } from "../lib/placeholder-records";

export default function RecordList({
  moduleLabel,
  modulePath,
  intro,
  items,
  q,
  status,
}: {
  moduleLabel: string;
  modulePath: string;
  intro: string;
  items: RecordDetail[];
  q?: string;
  status?: string;
}) {
  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">{moduleLabel}</span>
        <h2>{moduleLabel} module placeholder</h2>
        <p>{intro}</p>
      </section>

      <section className="section panel">
        <form className="grid" method="get">
          <label>
            <span className="eyebrow">Keyword</span>
            <input name="q" defaultValue={q ?? ""} placeholder="Search record no, customer, notes" />
          </label>
          <label>
            <span className="eyebrow">Status</span>
            <input name="status" defaultValue={status ?? ""} placeholder="draft / queued / received" />
          </label>
          <div>
            <span className="eyebrow">Apply</span>
            <button type="submit">Filter records</button>
          </div>
        </form>
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