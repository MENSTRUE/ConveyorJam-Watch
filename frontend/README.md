# Frontend — ConveyorJam Watch Control Center

A local-first React + TypeScript + Vite research UI. Intended design: industrial charcoal, copper/amber, sage accents. This is not an operational plant SCADA interface or safety alarm panel.

## Source of truth

- `src/App.tsx`: routes and layout.
- `src/pages/Overview.tsx`: summary activity and counts.
- `src/pages/Inspect.tsx`: image/video upload, inference device selection and output presentation.
- `src/pages/History.tsx`: SQLite-backed inspection list and clearing interaction.
- `src/pages/Settings.tsx`: change monitoring thresholds / ROI.
- `src/pages/Research.tsx`: research evidence and limitations.
- `src/api.ts`: HTTP methods / URL construction.
- `src/styles.css`: visual system; `package.json`: dependencies and scripts.

## Run

```powershell
cd frontend
npm ci
npm run dev
```

Vite defaults to `http://127.0.0.1:5173`. Start backend separately at `http://127.0.0.1:8000`; check Vite proxy configuration in `vite.config.ts`. Do not assume changing browser URL changes proxy. Run `npm run build` for TypeScript/Vite compile check; do not equate a successful build with successful media playback or inference.

## User journeys

1. **Overview:** inspect model availability, recent count of analyses and potential flags. These are local database counts, not a measured industrial fault rate.
2. **Inspect / image:** upload unannotated jpeg/png/webp, select Auto/CPU/CUDA as available, review detections and saved JPEG.
3. **Inspect / video:** upload short original video, set runtime options, run tracking, inspect playback and potential flags. Output media must be H.264 MP4 and served by backend.
4. **Archive:** navigate history and artifacts; deletion clears records, **not** media files.
5. **Settings:** adjust ROI and pixel/dwell thresholds. These are *heuristic* parameters and are not physically calibrated.
6. **Research:** distinguish Kaggle detector metrics from unverified jam events.

## Error states / UX acceptance

- Server offline: readable request error, no invented success badge.
- Missing champion model: show 503 and path guidance, not silent fallback to COCO detector.
- CUDA unavailable: no misleading GPU option; Auto must report effective device.
- Upload unsupported/too large: show validation response; no dangling spinner.
- Video encoding failure: return specific backend error, do not show a broken MP4 as success.
- Empty history: render actionable empty state; do not fake records.
- Production boundary: avoid red/green safety statuses for unverified alerts; label as **potential / unverified**.

## Tests / TODO

`npm run build` is the currently available compile check; this repository has no verified frontend unit/E2E suite. Priorities: component tests for states, integration test against FastAPI, Playwright upload/playback flow, keyboard navigation, responsive test, and slow-GPU timeout UX. Document passing evidence before marking Done.

## Deployment

Not production deployed. CORS defaults to local Vite origins. Public hosting requires HTTPS, access control, upload isolation, storage retention rules, media serving strategy, observability, and verified licensing. See [security and deployment](../docs/QUALITY_SECURITY_DEPLOYMENT.md).
