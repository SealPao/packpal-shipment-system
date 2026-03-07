import React from "react";

import RecordList from "../../components/record-list";
import { recordData } from "../../lib/placeholder-records";

export default function ReturnsPage() {
  return (
    <RecordList
      moduleLabel="Returns"
      modulePath="returns"
      intro="This page mirrors the planned return list contract and leaves room for condition review, reason analysis, and supporting attachments."
      items={recordData.returns}
    />
  );
}