import React from "react";

import RecordDetailPanel from "../../../components/record-detail-panel";
import { recordData } from "../../../lib/placeholder-records";

export default function ShipmentDetailPage({
  params,
}: {
  params: { recordId: string };
}) {
  return (
    <RecordDetailPanel
      moduleLabel="Shipments"
      detailLabel="Shipment Detail"
      emptyLabel="Shipment not found"
      item={recordData.shipments.find((entry) => entry.id === params.recordId)}
    />
  );
}