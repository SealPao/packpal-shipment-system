import React from "react";
import Link from "next/link";

import { recordData } from "../../lib/placeholder-records";

export default function ReturnsPage() {
  const items = recordData.returns;

  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Returns</span>
        <h2>Return module placeholder</h2>
        <p>
          This page mirrors the planned return list contract and leaves room for
          condition review, reason analysis, and supporting attachments.
        </p>
      </section>

      <section className="grid">
        {items.map((item) => (
          <article className="card panel" key={item.id}>
            <h3>{item.record_no}</h3>
            <p>{item.customer_name}</p>
            <p>Status: {item.status}</p>
            <p>
              <Link href={`/returns/${item.id}`}>View detail</Link>
            </p>
          </article>
        ))}
      </section>
    </main>
  );
}