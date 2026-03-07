import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "PackPal Web Admin",
  description: "Admin console skeleton for PackPal Shipment System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="zh-Hant">
      <body>
        <div className="shell">
          <header className="topbar">
            <div className="brand">
              <h1>PackPal Web Admin</h1>
              <p>出貨小幫手後台骨架，後續將串接查詢、管理與報表功能。</p>
            </div>
            <nav className="nav" aria-label="Primary">
              <Link href="/">Dashboard</Link>
              <Link href="/records">Records</Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
