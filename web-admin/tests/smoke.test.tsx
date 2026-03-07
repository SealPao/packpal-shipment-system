import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import DashboardPage from "../app/page";
import RecordsPage from "../app/records/page";

test("dashboard page renders expected text", () => {
  const html = renderToStaticMarkup(<DashboardPage />);

  assert.match(html, /Operational overview/);
  assert.match(html, /Shipment Workspace/);
  assert.match(html, /Repair Intake/);
});

test("records page renders expected text", () => {
  const html = renderToStaticMarkup(<RecordsPage />);

  assert.match(html, /Records placeholder/);
  assert.match(html, /Unified record table and filters/);
  assert.match(html, /Attachment preview and audit timeline/);
});