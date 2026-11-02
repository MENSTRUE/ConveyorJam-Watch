# Backend — ConveyorJam Watch

Run from repository root (Windows PowerShell):

```powershell
cd "D:\porto\100 day\day 29\ConveyorJam Watch"
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend/requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Swagger: http://localhost:8000/docs. Model file expected at `models/champion/conveyorjam_champion.pt` (kept local, Git-ignored). `GET /api/v1/health` works without the model; inference responds 503 if missing. Generated artifacts and SQLite history live under `backend/runtime/` and must never be committed. First model loading may be slow. Video uses YOLO+ByteTrack and a heuristic dwell threshold; **not** a validated industrial jam detector. No authentication or production-grade video processing queues.

Run tests: `cd backend; ..\.venv\Scripts\python -m pytest -q tests`.
