# AGENTS.md — ConveyorJam Watch Repository Contract

> **Mandatory instructions for human maintainers, AI coding agents, reviewers and automation.** Read this file and root `README.md` before changing this repository. The objective is an honest, reproducible **research prototype**, not a visually impressive but scientifically unsupported jam detector.

## A. Non-negotiable source-of-truth and scope

1. **Ground truth always wins.** Source-of-truth order: executed experimental artifacts (`reports/research/research_report.json`, `reports/evaluation/*`, `reports/audit/*`) → current code (`backend/app/main.py`, frontend files, tests) → original executed notebook/weights → observed local logs → docs → plans.
2. **Exact class semantics:** trained detector has **one class: `conveyor`**. It is **not** a material-item detector, stopped-belt detector, or physical-jam classifier. `potential_jam` is a low-motion **heuristic** derived from tracked detection-box centroids, not a verified event.
3. **No invented science:** never fabricate dataset sizes, split independence, training histories, metrics, plots, screenshots, demos, thresholds, hashes, video labels, licensing, citations, or test outcomes. If not measured, say **not measured**.
4. **No test-set shopping:** model comparison was selected on validation mAP50:95. Do not tune on held-out test. For next research iteration, pre-register a **new source-video/site separated holdout**.
5. **No safety/industrial-ready claims:** no verified jam labels, external-site validation, alarm F1/precision/recall, live monitoring SLA, or safety certification. Never connect rule output to machinery actuators or emergency controls.
6. **Respect external rights:** upstream datasets and footage have `NOT_VERIFIED` license statuses in existing evidence. Do not redistribute media/weights or claim upstream rights from repository MIT LICENSE.
7. **Never auto-import local data or move/delete staged files** unless expressly requested. No surprise file copying, Git pushes, remote commits, bulk deletion, license changes, or history rewrites.

## B. Actual project state as of 2026-11-02

- Repository: `MENSTRUE/ConveyorJam-Watch`, default branch `main`.
- Executed dataset source: `/kaggle/input/datasets/loliwibu/conveyorjam-dataset`, iron-ore YOLO source, class `conveyor`.
- Counts: train **2,283**, validation **96**, test **95** labeled positive images; **0 source negatives**.
- Validation models: YOLOv8n **0.989531** and YOLOv8s **0.990524** mAP50:95; selected YOLOv8s.
- Held-out source test: mAP50 **0.995**, mAP50:95 **0.9847654346**, precision **1.0**, recall **1.0**, source-video independence **unverified**.
- Three tested synthetic dwell scenarios passed; two recorded Kaggle iron-ore demo potential events are **UNVERIFIED**.
- Locally reported NVIDIA RTX 3050 Ti PyTorch CUDA run; one video generated, 161 observations, 0 potential flags, ~34.2 seconds; do **not** convert these into benchmark performance claims.
- Backend currently uses OpenCV `mp4v` intermediate → FFmpeg `libx264` H.264 output after `VideoWriter.release()`; this is source-verified, browser regression still to be measured.
- Existing GitHub repo contains accidentally tracked runtime SQLite, video backup and GPU patch backup. Preserve historical evidence, fix Git tracking deliberately.

## C. Required root and module boundaries

Canonical root: `README.md`, `AGENTS.md`, `LICENSE`, `.gitignore`, `.env.example`, `notebooks/`, `models/`, `reports/`, `assets/`, `backend/`, `frontend/`, `docs/`, `scripts/` and root `tests/` **only where they exist or have a purpose**. Do not create `datasets/` or invent files to make a tree look complete. Existing `backend/tests/` contains live tests; don't duplicate in root without a reason.

- `backend/app/main.py`: FastAPI endpoints, device selection, inference, tracker, dwell heuristic, SQLite, media transcoding.
- `backend/tests/test_api.py`: backend test contract.
- `frontend/src/pages/`: Overview, Inspect, History, Settings, Research. `src/api.ts` is API boundary; reuse existing request/response contracts.
- `models/champion/conveyorjam_champion.pt`: local-only checkpoint; DO NOT commit. Don't use random/pretrained COCO weights and label output as the fine-tuned champion.
- `reports/evaluation/`: observed detector metrics; `reports/research/`: study claim boundaries; `reports/audit/`: dataset provenance.
- `reports/video_analysis/potential_jam_events_UNVERIFIED.csv`: explicitly unverified candidate events.
- `assets/examples/images/`: *annotated* previews. `assets/examples/videos/`: *annotated* demo footage locally. `assets/examples/raw_images/` and `raw_videos/`: optional authorized, unannotated testing media. Never infer missing raw footage from output screenshots.
- `backend/runtime/`: mutable local media and `history.sqlite3`, not source code. Treat any previously committed runtime data as a repository hygiene issue.

## D. Engineering rules

- Python: maintain type annotations, small functions, explicit error handling, validated inputs, and stable API schemas. Avoid all-in-one feature additions without corresponding tests; full refactoring into modules may be proposed with compatibility plan.
- Frontend: React + TypeScript; use existing API client, error/loading/empty states; no fake realtime charts or hard-coded success indicators. Preserve industrial charcoal + amber/copper visual language for this project without reusing visual identities from unrelated apps.
- Keep inference selectable with `auto`, `cpu`, and `cuda:0`; CUDA only if PyTorch reports it. Do not label an unavailable device ready.
- Tracking: ByteTrack is stateful; isolate tracker state per video job. Protect any shared model's execution with sensible concurrency control. Do not rely on global Python in-memory settings as persisted config.
- Video: validate decode, source FPS, dimensions, time and file caps. Encode browser assets to H.264 `yuv420p` `+faststart`; close writer and capture first; fail explicitly on FFmpeg error. Retain the original processing timing separately from source/output FPS.
- File safety: never overwrite local raw media, notebook evidence, checkpoint or original audit files without an explicit backup + authorization. No `git add -f` for ignored large assets.
- APIs: do not change response fields or routes without updating frontend, docs and tests. Keep current `/api/v1` endpoints or publish a versioned migration.
- Security: current backend is **unauthenticated**; never expose it on a public host as-is. Use loopback only for local experimentation. Add controls before deployment.

## E. Model/data research protocol

1. Define user, industrial scenario, precise label semantics, camera conditions, and measurable outcome **before dataset/model choice**.
2. Get source data from trusted, verifiable origin with actual URL, version, license, attribution and accessed date. Record source limitations. Auxiliary datasets are not automatically ground truth.
3. Audit pairing, classes, object counts, null labels, duplicates, near duplicates, temporal/video overlap, orphan labels, corrupt files and annotation correctness.
4. Split **by video/site/time group** before any feature learning or training. If reproducing old source split, report its independence limits honestly.
5. Establish a simple baseline, then compare YOLO/temporal methods with fixed and documented splits. Track all hyperparameters, seed, software and hardware.
6. Select on validation only. Held-out test is read once after selection; for reused previous test, state "exploratory reused test".
7. Report precision, recall, AP/mAP and class support for **detector**; event precision/recall/latency only when independent **jam-event** labels exist.
8. Compare negative examples, difficult conveyor domains, weather/lighting and video group drift. Confidence intervals require appropriate unit-of-analysis and actual data.
9. Export actual executed checkpoint, manifests, metrics, plots, environment, model card and exact input/output recipes. Never claim an artifact exists if it wasn't created.
10. Verify model source license and derived weights terms before release. Keep raw and checkpoint data local unless explicit authorized distribution.

## F. Scope / risk / claim matrix

| Claim | Allowed? | Evidence required |
|---|---|---|
| One-class conveyor detection from iron-ore images | Yes | Current YOLO dataset + evaluation JSON |
| Source-test mAP50:95 0.9847654346 | Yes, qualified | State 95 positive images, unverified video independence |
| YOLOv8s chosen on validation | Yes | validation CSV |
| ByteTrack IDs produced in video | Yes, if observed | Processed tracking log/video |
| 2 candidate dwell events across recorded demos | Yes, **unverified only** | video event CSV and demo summary |
| Jam detector with 99% accuracy | **NO** | No real jam-event labeled evaluation |
| No false positives / no misses | **NO** | Neither negative nor jam-event ground truth |
| Industrial/factory safe, automated shutdown | **NO** | Requires independent industrial safety engineering |
| All third-party media can be redistributed | **NO** | License verification missing |

## G. Required testing gate for any PR

Always report which commands were **actually run**, environment, result and known gaps. Suggested local checks:

```powershell
.\.venv\Scripts\python -m py_compile backend\app\main.py
.\.venv\Scripts\python -m pytest backend\tests -q
.\.venv\Scripts\python -m pip check
cd frontend
npm ci
npm run build
```

For inference changes, test a valid unannotated JPEG and MP4, missing checkpoint, invalid ROI, large payload, FFmpeg unavailable, CPU-only mode, CUDA-capable mode where available, and a browser H.264 playback/seek check. For ML claims, verify evidence in `reports/` against original executed notebook. Do not fabricate green CI.

## H. Runtime & repository hygiene

- Keep `.env`, `.venv/`, `node_modules/`, `backend/runtime/`, `backend/tests/.runtime_test/`, `gpu_patch_backup/`, downloads, raw video and `.pt` out of Git.
- `.gitignore` does **not** untrack a file already committed. Inspect with `git ls-files`. Use `git rm --cached` with precise paths only after reviewing local contents and obtaining consent. Do not auto-delete existing SQLite evidence or third-party files.
- The project may contain pre-existing, committed sensitive local data. A future commit does not erase Git history; flag the issue rather than claiming permanent deletion.
- Use tracked documentation text and tiny non-sensitive research CSV/JSON/PNG only after checking provenance and permissions.
- Never add embedded credentials, private uploads, original footage, personal device paths, or private history records to README/examples/logs.

## I. Documentation requirements

Every changed feature requires updates to **README** and the appropriate module docs, plus a grounded test record. Every ML change requires corresponding manifest, experiment selection table, held-out evidence, limitations, and attribution. Use **Before–Now–Next** with precise dates, deliverables and objective acceptance criteria. Identify experimental, validated, proposed and deferred states. Keep API, configuration defaults and file paths synchronized with code.

When results contradict older docs, fix the docs and show evidence. Don't modify original logs or retroactively change experiment output. Do not claim 161 tracked unique objects if the counter sums observations.

## J. Development workflow and review format

For each task:

1. **Read** target files, AGENTS, README, source tests and research evidence.
2. **Plan** minimum change, touched files, API effects, data rights, safety/security risks.
3. **Implement** with small focused diffs. Do not change design theme, directory naming or unrelated data by default.
4. **Test** relevant unit, build, API/inference and playback paths as actually possible.
5. **Document** exact reproduction steps, before/after behavior, metrics, constraints and code links.
6. **Review** `git status`, `git diff --stat`, `git diff --check`, and ignored/tracked artifacts.
7. **Report** what passed, not tested, what to do next, and a precise recommended commit message.
8. **Push/PR** only if the user explicitly requests it. If connected GitHub writing is requested, inspect branch and current SHA; never silently overwrite remote updates.

A completed contribution summary should contain: *Task*, *Files changed*, *Observed tests*, *Behavior before vs after*, *Known limitations*, *Next validation*, and *Suggested commit message*.

## K. Planned architecture evolution (NOT yet implemented)

- Separate `backend/app/{api,services,models,tracking,storage,media}` modules.
- Persistent monitor configurations with validation/versioning.
- Correct event semantics using material motion or frame optical flow; independently labeled jams and stoppages.
- Asynchronous bounded job queue; progress and cancellation, upload quota and storage retention.
- Per-user authentication and RBAC, hardened media handling and observability.
- RTSP edge/industrial pilots only after data authorization, safety review, site-level evaluation.

Do not scaffold these folders solely to make the repository appear larger. Implement them only alongside tests, docs, and real needs.

## L. Definition of done

A task is **done** only when it meets the user's actual acceptance criterion, leaves the repository internally consistent, preserves original experimental evidence, passes available relevant checks, and does not misrepresent unverified functionality. If testing cannot be performed, say **implementation drafted, integration unverified** rather than *final production-ready*.

**Remember:** honest, traceable limitations are part of the engineering deliverable, not a flaw to hide.

## Documentation sync obligation

All documentation surfaces in [`docs/README.md`](docs/README.md), including `backend/README.md`, `frontend/README.md`, `docs/research/KAGGLE_OUTPUT_README.md`, `docs/id/README.md` and `docs/en/README.md`, must remain consistent with actual code and measured artifacts. Update the owning document when modifying a component; do not claim tests passed unless executed.
