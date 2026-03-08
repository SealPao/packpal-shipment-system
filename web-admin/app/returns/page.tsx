import React from "react";

import RecordList from "../../components/record-list";
import { filterRecords, recordData } from "../../lib/placeholder-records";

export default function ReturnsPage({
  searchParams,
}: {
  searchParams?: { q?: string; status?: string };
}) {
  const q = searchParams?.q;
  const status = searchParams?.status;

  return (
    <RecordList
      moduleLabel="Returns"
      modulePath="returns"
      intro="This page mirrors the planned return list contract and leaves room for condition review, reason analysis, and supporting attachments."
      items={filterRecords(recordData.returns, q, status)}
      q={q}
      status={status}
    />
  );
}