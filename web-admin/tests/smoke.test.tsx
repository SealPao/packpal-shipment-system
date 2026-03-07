import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import DashboardPage from "../app/page";
import RecordsPage from "../app/records/page";
import RepairsPage from "../app/repairs/page";
import RepairDetailPage from "../app/repairs/[recordId]/page";
import ReturnsPage from "../app/returns/page";
import ReturnDetailPage from "../app/returns/[recordId]/page";
import ShipmentsPage from "../app/shipments/page";
import ShipmentDetailPage from "../app/shipments/[recordId]/page";

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
});

test("shipments list page renders expected text", () => {
  const html = renderToStaticMarkup(<ShipmentsPage />);

  assert.match(html, /SHP-2026-0001/);
  assert.match(html, /View detail/);
});

test("shipment detail page renders expected text", () => {
  const html = renderToStaticMarkup(
    <ShipmentDetailPage params={{ recordId: "shipment-001" }} />,
  );

  assert.match(html, /Shipment Detail/);
  assert.match(html, /packing-slip/);
});

test("repairs list page renders expected text", () => {
  const html = renderToStaticMarkup(<RepairsPage />);

  assert.match(html, /RPR-2026-0001/);
  assert.match(html, /View detail/);
});

test("repair detail page renders expected text", () => {
  const html = renderToStaticMarkup(
    <RepairDetailPage params={{ recordId: "repair-001" }} />,
  );

  assert.match(html, /Repair Detail/);
  assert.match(html, /intake/);
});

test("returns list page renders expected text", () => {
  const html = renderToStaticMarkup(<ReturnsPage />);

  assert.match(html, /RTN-2026-0001/);
  assert.match(html, /View detail/);
});

test("return detail page renders expected text", () => {
  const html = renderToStaticMarkup(
    <ReturnDetailPage params={{ recordId: "return-001" }} />,
  );

  assert.match(html, /Return Detail/);
  assert.match(html, /damage-photo/);
});