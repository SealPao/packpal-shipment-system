import React from "react";
import Link from "next/link";

import { recordData } from "../../lib/placeholder-records";

export default function ShipmentsPage() {
  const items = recordData.shipments;

  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Shipments</span>
        <h2>Shipment module placeholder</h2>
        <p>
          This page now mirrors the planned list contract so the admin UI can
          evolve against a stable record summary shape.
        </p>
      </section>

      <section className="grid">
        {items.map((item) => (
          <article className="card panel" key={item.id}>
            <h3>{item.record_no}</h3>
            <p>{item.customer_name}</p>
            <p>Status: {item.status}</p>
            <p>Updated: {item.updated_at}</p>
            <p>
              <Link href={`/shipments/${item.id}`}>View detail</Link>
            </p>
          </article>
        ))}
      </section>
    </main>
  );
}