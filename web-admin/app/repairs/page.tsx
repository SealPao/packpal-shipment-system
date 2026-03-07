import React from "react";

import RecordList from "../../components/record-list";
import { recordData } from "../../lib/placeholder-records";

export default function RepairsPage() {
  return (
    <RecordList
      moduleLabel="Repairs"
      modulePath="repairs"
      intro="This page mirrors the planned repair list contract and leaves room for search, issue review, and attachment completeness checks."
      items={recordData.repairs}
    />
  );
}