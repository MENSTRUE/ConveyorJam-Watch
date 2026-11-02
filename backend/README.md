# Backend — ConveyorJam Watch API

> Research prototype only. The backend detects bounding boxes labeled `conveyor`, tracks them over sampled video frames, and raises *unverified* stationary-dwell signals. It is not a safety controller or validated jam classifier.

## Source of truth and runtime

- Implementation: [`app/main.py`](app/main.py).
- Unit/API tests: [`tests/test_api.py`](tests/test_api.py).
- Dependency declarations: [`requirements.txt`](requirements.txt); broad version bounds mean exact environments must be recorded separately.
- Local persistent data: `backend/runtime/history.sqlite3` and exported media; never commit these or upload private footage.
- Local champion: `../models/champion/conveyorjam_champion.pt`, intentionally excluded from Git.
- Full integration: [`../docs/API_AND_OPERATIONS.md`](../docs/API_AND_OPERATIONS.md).

## Install (PowerShell, repository root)

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
.\.venv\Scripts\python -m pip check
ffmpeg -version
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

For NVIDIA GPU use a **compatible CUDA-enabled PyTorch** version in this venv, then confirm `torch.cuda.is_available()`; having an NVIDIA driver alone is insufficient. A local RTX 3050 Ti successfully loaded the checkpoint on CUDA 12.8 / torch 2.10.0+cu128, but this is not a guaranteed dependency combination on every host.

## Endpoints

| Method | Path | Use |
|---|---|---|
| GET | `/api/v1/health` | Service, model and device state |
| GET / POST | `/api/v1/devices` | Inspect/set `auto`, `cpu`, `cuda:0` (selection is process-global) |
| GET / POST | `/api/v1/config` | Inspect/set in-memory dwell thresholds and normalized ROI |
| GET | `/api/v1/overview` | Counts and recent activity |
| GET | `/api/v1/history` | Recent analysis records |
| DELETE | `/api/v1/history` | Delete database records, not stored files |
| GET | `/api/v1/artifacts/{filename}` | Read existing `.jpg` or `.mp4` output |
| POST | `/api/v1/analyze/image` | Multipart `file` image detector |
| POST | `/api/v1/analyze/video` | Multipart `file`, optional `max_seconds`, `frame_stride` |

Interactive API schema: `http://127.0.0.1:8000/docs`. Image formats: jpg/jpeg/png/webp; video: mp4/avi/mov/mkv. Default maximum upload sizes 16 MiB image, 150 MiB video. Default max analyzed video duration 60s, request default 25s. Validate exact runtime response schemas against OpenAPI; documentation is not a generated client contract.

## Tracking and codec

The video path samples frames (default stride 3), invokes Ultralytics ByteTrack, tracks *conveyor region* IDs, applies a pixel-centroid stationary threshold and normalized ROI, and renders annotations. Current backend writes intermediate OpenCV `mp4v`, **releases the writer**, then runs FFmpeg `libx264`, `yuv420p`, `+faststart` before persisting final artifact. Requires FFmpeg on PATH with `libx264`. Browser-compatible `.mp4` is output, but browser playback must be smoke tested separately. Failure to transcode must not register a completed artifact.

Important research limitation: a conveyor can be stationary while **normal** (camera fixed), and moving material may not change its bounding box. Do not interpret dwell alerts as jams without independently labeled fault episodes.

## Configuration and persistence

Selected device and monitor settings are process-memory values and reset on restart. `YOLO_DEVICE` provides initial choice. Uploaded video bytes are temporarily written to disk and cleaned after processing. History uses SQLite and may include uploaded filenames, prediction metadata and events. Local instance has **no authentication**, no per-user tenant isolation, no queue, no documented retention policy, and no verified public deployment.

Supported environment variables: `CONVEYOR_MODEL`, `CONVEYOR_DATA_DIR`, `MAX_IMAGE_MB`, `MAX_VIDEO_MB`, `MAX_VIDEO_SECONDS`, `CONVEYOR_CONF`, `FRAME_STRIDE`, `YOLO_DEVICE`, `CORS_ORIGINS`. Check actual parsing in `app/main.py` before adding variables.

## Tests

```powershell
.\.venv\Scripts\python -m pytest backend\tests -q
.\.venv\Scripts\python -m py_compile backend\app\main.py
```

The current tests exercise health, config validation, missing-model error and a synthetic dwell positive case. They do **not** verify complete H.264 media playback, full GPU inference, attack surface or real jam F1. Add these tests before broadening claims. Run smoke tests with **unannotated**, properly licensed files, not Kaggle previews containing burned-in boxes.

## Troubleshooting

- `503 model missing`: verify local `.pt` path and `CONVEYOR_MODEL`.
- `409 CUDA unavailable`: check environment torch build and use CPU fallback.
- `FFmpeg not found`: install FFmpeg with `libx264`, verify PATH in server shell.
- MP4 exists but browser duration 0: inspect `ffprobe -show_streams`, codec `h264` / `avc1`, `yuv420p`, server media response; retry after reload.
- Tracking IDs unstable: scene motion, identity switches, ROI drift or domain shift; do not automatically count events as faults.
- Runtime sqlite/media unexpectedly tracked: remove from Git index using reviewed `git rm --cached`, add runtime ignore; deleting from current Git tree does not remove historic copies.

See [root README](../README.md), [research](../docs/RESEARCH_AND_DATA.md), [security](../docs/QUALITY_SECURITY_DEPLOYMENT.md).
