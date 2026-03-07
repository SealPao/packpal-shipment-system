import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import DashboardPage from "../app/page";
import RecordsPage from "../app/records/page";
import RepairsPage from "../app/repairs/page";
import ReturnsPage from "../app/returns/page";
import ShipmentsPage from "../app/shipments/page";

test("dashboard page renders expected text", () => {
  const html = renderToStaticMarkup(<DashboardPage />);

  assert.match(html, /Operational overview/);
  assert.match(html, /Shipment Workspace/);
  assert.match(html, /Open module/);
});

test("records page renders expected text", () => {
  const html = renderToStaticMarkup(<RecordsPage />);

  assert.match(html, /Records placeholder/);
  assert.match(html, /Unified record table and filters/);
  assert.match(html, /Attachment preview and audit timeline/);
});

test("shipments page renders expected text", () => {
  const html = renderToStaticMarkup(<ShipmentsPage />);

  assert.match(html, /Shipment module placeholder/);
  assert.match(html, /Upload and sync status visibility/);
});

test("repairs page renders expected text", () => {
  const html = renderToStaticMarkup(<RepairsPage />);

  assert.match(html, /Repair module placeholder/);
  assert.match(html, /Attachment completeness review/);
});

test("returns page renders expected text", () => {
  const html = renderToStaticMarkup(<ReturnsPage />);

  assert.match(html, /Return module placeholder/);
  assert.match(html, /Photo and document review panel/);
});