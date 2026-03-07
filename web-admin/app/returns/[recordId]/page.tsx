import React from "react";

import RecordDetailPanel from "../../../components/record-detail-panel";
import { recordData } from "../../../lib/placeholder-records";

export default function ReturnDetailPage({
  params,
}: {
  params: { recordId: string };
}) {
  return (
    <RecordDetailPanel
      moduleLabel="Returns"
      detailLabel="Return Detail"
      emptyLabel="Return not found"
      item={recordData.returns.find((entry) => entry.id === params.recordId)}
    />
  );
}