import React from "react";

import RecordDetailPanel from "../../../components/record-detail-panel";
import { recordData } from "../../../lib/placeholder-records";

export default function RepairDetailPage({
  params,
}: {
  params: { recordId: string };
}) {
  return (
    <RecordDetailPanel
      moduleLabel="Repairs"
      detailLabel="Repair Detail"
      emptyLabel="Repair not found"
      item={recordData.repairs.find((entry) => entry.id === params.recordId)}
    />
  );
}