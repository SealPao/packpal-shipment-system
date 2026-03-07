import React from "react";
import Link from "next/link";

import { recordData } from "../../lib/placeholder-records";

export default function RepairsPage() {
  const items = recordData.repairs;

  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Repairs</span>
        <h2>Repair module placeholder</h2>
        <p>
          This page mirrors the planned repair list contract and leaves room for
          search, issue review, and attachment completeness checks.
        </p>
      </section>

      <section className="grid">
        {items.map((item) => (
          <article className="card panel" key={item.id}>
            <h3>{item.record_no}</h3>
            <p>{item.customer_name}</p>
            <p>Status: {item.status}</p>
            <p>
              <Link href={`/repairs/${item.id}`}>View detail</Link>
            </p>
          </article>
        ))}
      </section>
    </main>
  );
}