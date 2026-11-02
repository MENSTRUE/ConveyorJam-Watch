from __future__ import annotations

import json
import math
import os
import subprocess
import shutil
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = Path(os.getenv("CONVEYOR_MODEL", str(ROOT / "models" / "champion" / "conveyorjam_champion.pt")))
DATA_DIR = Path(os.getenv("CONVEYOR_DATA_DIR", str(ROOT / "backend" / "runtime"))).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "history.sqlite3"
MAX_IMAGE_BYTES = int(os.getenv("MAX_IMAGE_MB", "16")) * 1024**2
MAX_VIDEO_BYTES = int(os.getenv("MAX_VIDEO_MB", "150")) * 1024**2
MAX_VIDEO_SECONDS = float(os.getenv("MAX_VIDEO_SECONDS", "60"))
CONFIDENCE = float(os.getenv("CONVEYOR_CONF", "0.25"))
FRAME_STRIDE = max(1, int(os.getenv("FRAME_STRIDE", "3")))
DEVICE = os.getenv("YOLO_DEVICE", "auto").strip().lower()
if DEVICE not in {"auto", "cpu", "cuda:0"}:
    DEVICE = "auto"


def compute_capabilities() -> dict:
    try:
        import torch
        available = bool(torch.cuda.is_available())
        return {
            "cuda_available": available,
            "gpu_name": str(torch.cuda.get_device_name(0)) if available else None,
            "torch_version": str(torch.__version__),
            "torch_cuda_version": str(torch.version.cuda) if torch.version.cuda else None,
        }
    except Exception:
        return {"cuda_available": False, "gpu_name": None, "torch_version": None, "torch_cuda_version": None}


def resolved_device() -> str:
    caps = compute_capabilities()
    if DEVICE == "cuda:0" and not caps["cuda_available"]:
        raise HTTPException(409, "CUDA GPU unavailable. Install a CUDA-enabled PyTorch build or switch to CPU.")
    return "cuda:0" if DEVICE == "auto" and caps["cuda_available"] else ("cpu" if DEVICE == "auto" else DEVICE)


class DeviceSelection(BaseModel):
    device: str


app = FastAPI(title="ConveyorJam Watch API", version="1.0.0", description="Research prototype: conveyor detection, tracking and heuristic anomaly flags")
origins = [s.strip() for s in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if s.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST", "DELETE"], allow_headers=["Content-Type"])
_model: Any = None
_model_error: str | None = None
_model_lock = threading.Lock()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def setup_db():
    with db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS analyses (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, kind TEXT NOT NULL, status TEXT NOT NULL, filename TEXT NOT NULL, detections INTEGER NOT NULL, alerts INTEGER NOT NULL, processing_seconds REAL NOT NULL, details TEXT NOT NULL, artifact TEXT)")


setup_db()


def get_model():
    global _model, _model_error
    if _model is not None:
        return _model
    if not MODEL_PATH.is_file():
        raise HTTPException(503, f"Champion model missing. Expected local file: {MODEL_PATH}")
    with _model_lock:
        if _model is None:
            try:
                from ultralytics import YOLO
                _model = YOLO(str(MODEL_PATH))
                _model_error = None
            except Exception as exc:
                _model_error = f"{type(exc).__name__}: {exc}"
                raise HTTPException(503, f"Model load failed: {_model_error}") from exc
    return _model


def save_record(kind: str, filename: str, detections: int, alerts: int, elapsed: float, details: dict, artifact: str | None = None) -> dict:
    record = dict(id=uuid.uuid4().hex[:12], created_at=now(), kind=kind, status="completed", filename=filename[:200], detections=detections, alerts=alerts, processing_seconds=round(elapsed, 3), details=details, artifact=artifact)
    with db() as conn:
        conn.execute("INSERT INTO analyses VALUES (:id,:created_at,:kind,:status,:filename,:detections,:alerts,:processing_seconds,:details,:artifact)", {**record, "details": json.dumps(details, default=str)})
    return record


def ensure_media(filename: str | None, allowed: set[str], content_type: str):
    suffix = Path(filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(415, f"Unsupported file extension: {suffix}. Allowed: {sorted(allowed)}")
    # Browser MIME is advisory; actual decoding is verified independently.
    return suffix


async def read_upload(upload: UploadFile, maximum: int) -> bytes:
    data = await upload.read(maximum + 1)
    if not data:
        raise HTTPException(400, "Empty upload")
    if len(data) > maximum:
        raise HTTPException(413, "File exceeds upload limit")
    return data


def boxes_from(result) -> list[dict]:
    predictions = []
    if result.boxes is None:
        return predictions
    names = result.names
    for box in result.boxes:
        coords = [round(float(v), 1) for v in box.xyxy[0].cpu().tolist()]
        cls = int(box.cls[0].item())
        predictions.append({"class_id": cls, "label": str(names.get(cls, cls) if isinstance(names, dict) else names[cls]), "confidence": round(float(box.conf[0].item()), 4), "bbox": coords, "track_id": int(box.id[0].item()) if box.id is not None else None})
    return predictions


def overlay(frame: np.ndarray, detections: list[dict], headline: str, alerts: int = 0) -> np.ndarray:
    img = frame.copy()
    cv2.rectangle(img, (0, 0), (min(img.shape[1], 900), 58), (24, 29, 35), -1)
    cv2.putText(img, headline[:85], (16, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (236, 237, 245), 2, cv2.LINE_AA)
    for obj in detections:
        x1, y1, x2, y2 = (int(v) for v in obj["bbox"])
        col = (47, 176, 244) if alerts == 0 else (42, 78, 255)
        cv2.rectangle(img, (x1, y1), (x2, y2), col, 2)
        txt = f'{obj["label"]} {obj["confidence"]:.2f}'
        if obj.get("track_id") is not None:
            txt = f'#{obj["track_id"]} ' + txt
        cv2.putText(img, txt, (x1, max(72, y1 - 9)), cv2.FONT_HERSHEY_SIMPLEX, .56, col, 2, cv2.LINE_AA)
    return img


class MonitorConfig(BaseModel):
    dwell_seconds: float = Field(default=3.0, ge=0.5, le=60)
    stationary_px_per_second: float = Field(default=12.0, ge=0.1, le=500)
    roi: tuple[float, float, float, float] = (0.04, 0.08, 0.96, 0.94)
    min_observations: int = Field(default=4, ge=2, le=100)
    lost_reset_seconds: float = Field(default=1.0, ge=0.1, le=10)


CONFIG = MonitorConfig()


def validate_roi(roi: tuple[float, float, float, float]):
    x1, y1, x2, y2 = roi
    if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
        raise HTTPException(422, "ROI must satisfy 0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1")


class DwellEngine:
    def __init__(self, config: MonitorConfig, width: int, height: int):
        self.config = config
        self.width = width
        self.height = height
        self.states: dict[int, dict] = {}
        self.events: list[dict] = []

    def update(self, detections: list[dict], timestamp: float) -> list[dict]:
        active = set()
        current = []
        xlo, ylo, xhi, yhi = self.config.roi
        for obj in detections:
            tid = obj.get("track_id")
            if tid is None:
                continue
            active.add(tid)
            x1, y1, x2, y2 = obj["bbox"]
            center = ((x1+x2)/2, (y1+y2)/2)
            if not (xlo*self.width <= center[0] <= xhi*self.width and ylo*self.height <= center[1] <= yhi*self.height):
                self.states.pop(tid, None)
                continue
            state = self.states.get(tid)
            if state is None or timestamp - state["time"] > self.config.lost_reset_seconds:
                self.states[tid] = {"center": center, "time": timestamp, "speed_history": [], "since": None, "count": 1, "alerted": False}
                obj["dwell_seconds"] = 0.0
                obj["potential_jam"] = False
                current.append(obj)
                continue
            dt = timestamp - state["time"]
            speed = math.dist(center, state["center"]) / dt if dt > 1e-6 else float("inf")
            state["speed_history"].append(speed)
            state["speed_history"] = state["speed_history"][-5:]
            state["count"] += 1
            stationary = state["count"] >= self.config.min_observations and float(np.median(state["speed_history"])) <= self.config.stationary_px_per_second
            if stationary:
                if state["since"] is None:
                    state["since"] = timestamp
                dwell = timestamp - state["since"]
                if dwell >= self.config.dwell_seconds and not state["alerted"]:
                    state["alerted"] = True
                    self.events.append({"track_id": tid, "time_seconds": round(timestamp, 2), "class": obj["label"], "reason": "stationary_dwell_threshold", "verified_jam": False})
            else:
                dwell = 0
                state["since"] = None
                state["alerted"] = False
            state["time"] = timestamp
            state["center"] = center
            obj["dwell_seconds"] = round(dwell, 2)
            obj["potential_jam"] = state["alerted"]
            current.append(obj)
        for tid, state in list(self.states.items()):
            if tid not in active and timestamp - state["time"] > self.config.lost_reset_seconds:
                del self.states[tid]
        return current


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "model_ready": MODEL_PATH.is_file(), "model_loaded": _model is not None, "model_path": str(MODEL_PATH), "model_error": _model_error, "device": resolved_device() if DEVICE != "cuda:0" or compute_capabilities()["cuda_available"] else "unavailable", "device_selection": DEVICE, "compute": compute_capabilities(), "service": "ConveyorJam Watch", "mode": "research-prototype", "timestamp": now()}


@app.get("/api/v1/devices")
def devices():
    caps = compute_capabilities()
    return {"selection": DEVICE, "effective_device": resolved_device() if DEVICE != "cuda:0" or caps["cuda_available"] else "unavailable", **caps, "options": ["auto", "cpu"] + (["cuda:0"] if caps["cuda_available"] else [])}


@app.post("/api/v1/devices")
def device_set(request: DeviceSelection):
    global DEVICE
    selection = request.device.strip().lower()
    if selection not in {"auto", "cpu", "cuda:0"}:
        raise HTTPException(422, "Choose auto, cpu, or cuda:0")
    with _model_lock:
        if selection == "cuda:0" and not compute_capabilities()["cuda_available"]:
            raise HTTPException(409, "CUDA GPU unavailable with the current PyTorch installation")
        DEVICE = selection
    return devices()


@app.get("/api/v1/config")
def config_get():
    return CONFIG.model_dump()


@app.post("/api/v1/config")
def config_set(value: MonitorConfig):
    global CONFIG
    validate_roi(value.roi)
    CONFIG = value
    return CONFIG.model_dump()


@app.get("/api/v1/overview")
def overview():
    with db() as conn:
        stats = conn.execute("SELECT COUNT(*) AS analyses, COALESCE(SUM(alerts),0) AS alerts, COALESCE(SUM(detections),0) AS detections FROM analyses").fetchone()
        by_day = conn.execute("SELECT SUBSTR(created_at,1,10) AS day, COUNT(*) AS analyses, SUM(alerts) AS alerts FROM analyses GROUP BY day ORDER BY day DESC LIMIT 14").fetchall()
    return {"stats": dict(stats), "activity": [dict(r) for r in reversed(by_day)], "model_ready": MODEL_PATH.is_file(), "notice": "Flags are heuristic potential jams, not verified physical conveyor faults."}


@app.get("/api/v1/history")
def history(limit: int = 30):
    limit = min(max(limit, 1), 100)
    with db() as conn:
        rows = conn.execute("SELECT * FROM analyses ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return [{**dict(r), "details": json.loads(r["details"])} for r in rows]


@app.delete("/api/v1/history")
def history_clear():
    with db() as conn:
        conn.execute("DELETE FROM analyses")
    return {"status": "cleared", "note": "Exported artifact files are intentionally retained."}


@app.get("/api/v1/artifacts/{filename}")
def artifact(filename: str):
    if not filename or filename != Path(filename).name:
        raise HTTPException(400, "Invalid artifact name")
    path = DATA_DIR / filename
    if path.suffix not in {".jpg", ".mp4"} or not path.is_file():
        raise HTTPException(404, "Artifact not found")
    return FileResponse(path, media_type="image/jpeg" if path.suffix == ".jpg" else "video/mp4", filename=path.name, content_disposition_type="inline")


@app.post("/api/v1/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    ensure_media(file.filename, {".jpg", ".jpeg", ".png", ".webp"}, file.content_type or "")
    raw = await read_upload(file, MAX_IMAGE_BYTES)
    image = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(422, "Image decoding failed")
    if image.shape[0] * image.shape[1] > 30_000_000:
        raise HTTPException(413, "Image dimensions too large")
    device = resolved_device()
    model = get_model()
    start = time.perf_counter()
    with _model_lock:
        result = model.predict(image, conf=CONFIDENCE, imgsz=640, device=device, verbose=False)[0]
    objects = boxes_from(result)
    rendered = overlay(image, objects, f"CONVEYOR SCAN / {len(objects)} objects")
    artifact_name = uuid.uuid4().hex[:16] + ".jpg"
    if not cv2.imwrite(str(DATA_DIR / artifact_name), rendered):
        raise HTTPException(500, "Could not save annotation")
    elapsed = time.perf_counter() - start
    record = save_record("image", file.filename or "uploaded image", len(objects), 0, elapsed, {"width": image.shape[1], "height": image.shape[0], "objects": objects, "note": "Object detection alone cannot determine physical jam status."}, artifact_name)
    return {**record, "artifact_url": f"/api/v1/artifacts/{artifact_name}"}


@app.post("/api/v1/analyze/video")
async def analyze_video(
    file: UploadFile = File(...),
    max_seconds: float = Form(25),
    frame_stride: int = Form(FRAME_STRIDE),
):
    ensure_media(file.filename, {".mp4", ".avi", ".mov", ".mkv"}, file.content_type or "")
    if not (1 <= max_seconds <= MAX_VIDEO_SECONDS):
        raise HTTPException(422, f"max_seconds must be 1-{MAX_VIDEO_SECONDS}")
    if not 1 <= frame_stride <= 12:
        raise HTTPException(422, "frame_stride must be 1-12")

    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin is None:
        raise HTTPException(503, "FFmpeg not found in PATH. Install FFmpeg with libx264 to export browser-playable video.")

    raw = await read_upload(file, MAX_VIDEO_BYTES)
    suffix = Path(file.filename or "video.mp4").suffix.lower()
    job_id = uuid.uuid4().hex[:16]
    upload_path = DATA_DIR / f"{job_id}_upload{suffix}"
    intermediate_path = DATA_DIR / f"{job_id}_tracking_mp4v.mp4"
    output_name = f"{job_id}.mp4"
    output_path = DATA_DIR / output_name

    device = resolved_device()
    # Verify the champion exists before creating any runtime artifacts.
    get_model()
    upload_path.write_bytes(raw)
    cap = None
    writer = None
    finished = False
    start = time.perf_counter()

    try:
        cap = cv2.VideoCapture(str(upload_path))
        if not cap.isOpened():
            raise HTTPException(422, "Video decoding failed")
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if not math.isfinite(fps) or fps <= 0 or width <= 0 or height <= 0 or width * height > 9_000_000:
            raise HTTPException(422, "Invalid FPS or video dimensions")

        output_fps = max(1.0, fps / frame_stride)
        writer = cv2.VideoWriter(
            str(intermediate_path), cv2.VideoWriter_fourcc(*"mp4v"), output_fps, (width, height)
        )
        if not writer.isOpened():
            raise HTTPException(500, "Intermediate MP4 encoder unavailable")

        config_snapshot = CONFIG.model_copy(deep=True)
        engine = DwellEngine(config_snapshot, width, height)
        frame_index = 0
        processed = 0
        observations = 0
        total_frames = min(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or int(fps * max_seconds), int(fps * max_seconds))
        from ultralytics import YOLO
        tracking_model = YOLO(str(MODEL_PATH))

        with _model_lock:
            while frame_index < total_frames:
                ok, frame = cap.read()
                if not ok:
                    break
                i = frame_index
                frame_index += 1
                if i % frame_stride:
                    continue
                result = tracking_model.track(
                    frame, persist=True, tracker="bytetrack.yaml",
                    conf=CONFIDENCE, imgsz=640, device=device, verbose=False,
                )[0]
                objects = boxes_from(result)
                timestamp = i / fps
                tracked = engine.update(objects, timestamp)
                observations += len(objects)
                active_flags = sum(int(o.get("potential_jam", False)) for o in tracked)
                rendered = overlay(frame, objects, f"TRACKING / {timestamp:05.1f}s / active flags: {active_flags}", active_flags)
                x1, y1, x2, y2 = config_snapshot.roi
                cv2.rectangle(rendered, (int(x1*width), int(y1*height)), (int(x2*width), int(y2*height)), (60, 193, 230), 2)
                writer.write(rendered)
                processed += 1

        if processed == 0:
            raise HTTPException(422, "No video frames processed")

        # IMPORTANT: OpenCV must finalize the container before FFmpeg reads it.
        writer.release()
        writer = None
        cap.release()
        cap = None
        if not intermediate_path.is_file() or intermediate_path.stat().st_size == 0:
            raise HTTPException(500, "Tracking video output was empty")

        command = [
            ffmpeg_bin, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-i", str(intermediate_path),
            "-map", "0:v:0", "-an", "-c:v", "libx264",
            "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(output_path),
        ]
        try:
            conversion = subprocess.run(command, capture_output=True, text=True, timeout=180, check=False)
        except subprocess.TimeoutExpired as exc:
            raise HTTPException(500, "H.264 video conversion timed out") from exc
        except OSError as exc:
            raise HTTPException(500, f"Cannot run FFmpeg: {exc}") from exc

        if conversion.returncode != 0 or not output_path.is_file() or output_path.stat().st_size == 0:
            error = (conversion.stderr or "Unknown FFmpeg error")[-1200:]
            raise HTTPException(500, f"H.264 conversion failed: {error}")

        elapsed = time.perf_counter() - start
        details = {
            "source_fps": round(fps, 2),
            "output_fps": round(output_fps, 2),
            "processed_frames": processed,
            "duration_seconds": round(frame_index / fps, 2),
            "tracking_observations": observations,
            "events": engine.events,
            "processing_fps": round(processed / max(elapsed, 0.001), 2),
            "config": config_snapshot.model_dump(),
            "video_codec": "h264",
            "video_pixel_format": "yuv420p",
            "verified_jam_ground_truth": False,
        }
        record = save_record(
            "video", file.filename or "uploaded video", observations,
            len(engine.events), elapsed, details, output_name,
        )
        finished = True
        return {**record, "artifact_url": f"/api/v1/artifacts/{output_name}"}
    finally:
        if cap is not None:
            cap.release()
        if writer is not None:
            writer.release()
        upload_path.unlink(missing_ok=True)
        intermediate_path.unlink(missing_ok=True)
        if not finished:
            output_path.unlink(missing_ok=True)
