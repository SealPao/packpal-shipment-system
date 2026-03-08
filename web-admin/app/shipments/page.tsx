import React from "react";

import RecordList from "../../components/record-list";
import { filterRecords, recordData } from "../../lib/placeholder-records";

export default function ShipmentsPage({
  searchParams,
}: {
  searchParams?: { q?: string; status?: string };
}) {
  const q = searchParams?.q;
  const status = searchParams?.status;

  return (
    <RecordList
      moduleLabel="Shipments"
      modulePath="shipments"
      intro="This page now mirrors the planned list contract so the admin UI can evolve against a stable record summary shape."
      items={filterRecords(recordData.shipments, q, status)}
      q={q}
      status={status}
    />
  );
}