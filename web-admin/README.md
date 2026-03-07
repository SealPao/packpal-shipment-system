# Web Admin

Next.js admin skeleton for PackPal Shipment System.

## Structure

- `app/layout.tsx`: shared layout and navigation
- `app/page.tsx`: dashboard placeholder
- `app/records/page.tsx`: records placeholder
- `app/globals.css`: base theme and layout styling
- `tests`: minimal page smoke tests

## Run

```powershell
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Test

```powershell
npm install
npm test
```

## Current Scope

Included:
- Basic admin layout
- Dashboard shell
- Records page placeholder
- Smoke tests for the dashboard and records pages

Deferred:
- Authentication
- Real API calls
- Search, filtering, and detail views