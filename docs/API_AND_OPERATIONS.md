# API and Local Operations Runbook

**Source:** inspected `backend/app/main.py` on GitHub default branch 2026-11-02. API is designed for trusted local development, not public hosting.

## Architecture

React/Vite (`frontend/src`) sends Axios requests to FastAPI (`backend/app/main.py`). FastAPI loads the fine-tuned YOLO checkpoint, performs image detection or video ByteTrack, and stores inspection metadata in local SQLite. Annotated image outputs are JPEG. Video writes an intermediate OpenCV `mp4v` file, then runs FFmpeg to create H.264/yuv420p/faststart and returns an artifact URL.

## Start

```powershell
cd "D:\porto\100 day\day 29\ConveyorJam Watch"
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --reload --port 8000
```

In another terminal:

```powershell
cd "D:\porto\100 day\day 29\ConveyorJam Watch\frontend"
npm ci
npm run dev
```

Backend Swagger: `http://127.0.0.1:8000/docs`; frontend `http://127.0.0.1:5173`.

## Endpoint contract

| Endpoint | Input | Output/behavior |
|---|---|---|
| `GET /api/v1/health` | — | service status, checkpoint exists, device and CUDA capabilities |
| `GET /api/v1/devices` | — | current selection, effective device, allowed options |
| `POST /api/v1/devices` | JSON `device: auto/cpu/cuda:0` | updates in-memory choice; CUDA selection denied when unavailable |
| `GET/POST /api/v1/config` | Pydantic config body for POST | ROI and dwell parameters, not persistent across restarts |
| `GET /api/v1/overview` | — | historical counts and per-day aggregates |
| `GET /api/v1/history?limit=30` | max 100 | persisted history rows with JSON details |
| `DELETE /api/v1/history` | — | removes SQLite rows, **not media files** |
| `GET /api/v1/artifacts/{filename}` | JPG/MP4 basename | inline browser media file |
| `POST /api/v1/analyze/image` | multipart `file`; JPG/JPEG/PNG/WebP | detector boxes and JPEG artifact URL |
| `POST /api/v1/analyze/video` | multipart `file`, `max_seconds`, `frame_stride`; MP4/AVI/MOV/MKV | tracking observations, heuristic events and H.264 artifact URL |

Actual parameter defaults are from Python, not arbitrary UI labels: image 16 MB, video 150 MB, max video 60 seconds, default requested segment 25 seconds, frame stride 3, confidence 0.25, img size 640. `MAX_*` are environment-configurable.

## Device check

```powershell
nvidia-smi
.\.venv\Scripts\python -c "import torch; print(torch.__version__,torch.version.cuda,torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Do not change `device` UI label without verifying runtime `effective_device`. The fine-tuned model file is required at `models/champion/conveyorjam_champion.pt` unless `CONVEYOR_MODEL` changes it.

## Video codec acceptance

```powershell
ffmpeg -version
ffmpeg -encoders | Select-String libx264
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt,width,height -show_entries format=duration -of json "backend\runtime\OUTPUT.mp4"
```

Expected: `codec_name: h264`, `pix_fmt: yuv420p`, positive duration, file served by `/api/v1/artifacts/`, playable/seekable in Edge/Chrome. `mp4v` is a video codec distinct from MP4 *container* and may not be supported by browsers. Never transcode while OpenCV writer is open.

## Operational risks

- No authentication, no per-user permissions and no public deployment safety. Restrict to loopback.
- Database history is mutable and may contain uploaded filenames; take appropriate privacy measures.
- Uploaded video decoding can consume CPU/RAM/GPU; size and duration limits do not constitute full sandboxing.
- H.264 conversion uses CPU `libx264` by default; GPU detector speed does not imply video export speed.
- A stationary conveyor bounding box can be *normal*; alert events are not validated jams.
- For external video tests obtain permission, source attribution and independent sampling. Annotated Kaggle demos are not raw test data.

## Emergency debugging sequence

1. Reproduce with shortest authorized raw input.
2. Check `/health` and `/devices`.
3. Confirm checkpoint exists and PyTorch CUDA mode is correct.
4. Inspect FastAPI logs, HTTP status and browser Network/Console.
5. Confirm artifact path and FFmpeg codec; avoid overwriting evidence without backup.
6. Test CPU mode when CUDA OOM occurs; don't repeatedly restart without reading logs.
7. Save minimal non-sensitive reproduction and corresponding code change as a test.
