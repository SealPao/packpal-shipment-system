import React from "react";

import RecordList from "../../components/record-list";
import { recordData } from "../../lib/placeholder-records";

export default function ShipmentsPage() {
  return (
    <RecordList
      moduleLabel="Shipments"
      modulePath="shipments"
      intro="This page now mirrors the planned list contract so the admin UI can evolve against a stable record summary shape."
      items={recordData.shipments}
    />
  );
}