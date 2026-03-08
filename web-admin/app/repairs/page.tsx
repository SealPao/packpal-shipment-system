import React from "react";

import RecordList from "../../components/record-list";
import { filterRecords, recordData } from "../../lib/placeholder-records";

export default function RepairsPage({
  searchParams,
}: {
  searchParams?: { q?: string; status?: string };
}) {
  const q = searchParams?.q;
  const status = searchParams?.status;

  return (
    <RecordList
      moduleLabel="Repairs"
      modulePath="repairs"
      intro="This page mirrors the planned repair list contract and leaves room for search, issue review, and attachment completeness checks."
      items={filterRecords(recordData.repairs, q, status)}
      q={q}
      status={status}
    />
  );
}