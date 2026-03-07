import React from "react";

export default function ShipmentsPage() {
  return (
    <main>
      <section className="hero panel">
        <span className="eyebrow">Shipments</span>
        <h2>Shipment module placeholder</h2>
        <p>
          This page will host shipment-centric admin workflows once the backend
          contracts for shipment records and media are finalized.
        </p>
      </section>

      <section className="section panel">
        <h3>Planned capabilities</h3>
        <ul className="placeholder-list">
          <li>Shipment record list and search filters</li>
          <li>Snapshot and video preview panel</li>
          <li>Upload and sync status visibility</li>
        </ul>
      </section>
    </main>
  );
}