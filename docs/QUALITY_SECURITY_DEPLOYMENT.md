# Quality, Security, Testing and Deployment Gates

## Quality checklist

- Scope of each prediction is explicitly defined: conveyor **bounding box** and possible track ID; heuristic flag is **unverified**.
- API and frontend types match current `/api/v1` routes.
- Tests check normal and invalid input, deterministic synthetic dwell paths, and model-unavailable behavior.
- CUDA/CPU switching must not silently use a different unintended checkpoint.
- Every output JPG/MP4 can be opened; H.264 video includes seekable playback metadata.
- No runtime SQLite/video/backup, unauthorized source footage, or model weights are pushed.
- UI empty/error/loading states reflect true backend responses.
- A clear operator warning prevents presenting heuristic flags as verified faults.

## Commands

```powershell
cd "D:\porto\100 day\day 29\ConveyorJam Watch"
.\.venv\Scripts\python -m py_compile backend\app\main.py
.\.venv\Scripts\python -m pytest backend\tests -q
.\.venv\Scripts\python -m pip check
cd frontend
npm ci
npm run build
cd ..
git diff --check
git status --short
git ls-files backend/runtime gpu_patch_backup
```

These are **proposed checks**, not proof that CI passed; document actual command outputs and execution environment.

## Security blockers before deployment

1. Authentication and role permissions on all routes. `DELETE /history`, config/device mutation, and artifact retrieval must not be available to strangers.
2. Untrusted media upload isolation, decoding constraints, content-type verification, bounded operations, timeouts, and resource controls.
3. Data protection: privacy notice, purpose restriction, consent/authority, media retention and deletion, audit logs, encryption at rest and in transit where appropriate.
4. Central request logging with secrets/PII redaction, trace IDs, monitoring, alerts and operational runbooks.
5. Request quotas, asynchronous job queue and concurrency capacity planning; avoid blocking all requests with long video inference.
6. Secure storage lifecycle: generated files, errors, garbage collection, backups, quotas and least-privilege filesystem permissions.
7. Reproducible dependency lockfiles, vulnerability monitoring and release signatures. Validate proprietary and upstream licensing.
8. Industrial safety assessment and operator authority separation; this prototype must never drive critical machine actuators.

## Deployment maturity levels

| Level | Description | Current |
|---|---|---|
| L0 | Local research / demonstration | **Yes** (local app implemented, one video run observed) |
| L1 | Repeatable test suite and CI on clean runner | Not verified |
| L2 | Authenticated staging with reproducible packaging | Not implemented |
| L3 | Independently jam-labeled external test and calibration | Not available |
| L4 | Authorized industrial pilot with human oversight | Not available |
| L5 | Safety-engineered certified production use | Not claimed |

## Definition of done for next release

Collect an authorized independent media set, remove tracked runtime/backup files from future commits with a reviewed change, run backend/frontend builds, add an automated H.264 probe and playback smoke test, implement structured error handling, and publish a provenance ledger. Do not call the project production-ready without an externally evaluated jam-event detection protocol.

## Data/claims governance

- Detection AP reported for **95 source positive test images** only.
- Dwell synthetic tests are unit scenarios, not physical fault measurement.
- Jam-event precision, recall, macro-F1, false-positive rate, event detection delay and uncertainty are **not measured**.
- Runtime or manufacturing availability SLA is **not measured**.
- Zero alerts is **not equivalent** to no jam.
- Source video rights are `NOT_VERIFIED` per original dataset provenance.
