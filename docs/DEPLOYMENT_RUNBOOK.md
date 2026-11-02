# Local Operations and Deployment Runbook

**Release label:** local research prototype only. Do not attach this directly to industrial line control, emergency shutdown, regulated safety processes or public unauthenticated internet.

## Local start

PowerShell root:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Verify `/api/v1/health`, `/api/v1/devices`, `/docs`, and UI upload/playback. `--reload` is a development flag; not a deployment specification. To bind other interfaces, design authentication and network policy first.

## GPU operational checks

`nvidia-smi` confirms driver recognition; torch CUDA build recognition is separate. `CUDA Available: True` and YOLO model parameters on `cuda:0` confirmed locally on an RTX 3050 Ti; runtime GPU memory is limited (~4 GiB), so prefer one short video, stride 3, batch 1 and bounded input resolution. Monitor peak memory, video processing latency and upload size before increasing workloads.

## Reliability and retention

Uploaded media is read into memory up to the configured upload cap; code is synchronous GPU work in a request handler. Local SQLite, process-global selection/settings and filesystem media storage are not horizontally scalable. No automatic artifact cleanup/TTL, backups, database migrations, work queue, per-user isolation or circuit breaker is proven. Keep `backend/runtime/` outside Git, back it up only if necessary, and define retention/purge before real use.

## Operational failure table

| Failure | Detection | Action |
|---|---|---|
| Model missing | 503 / health `model_ready=false` | Check checkpoint path; obtain authorized weights |
| CUDA absent | 409 / health compute false | Switch CPU; inspect torch build |
| FFmpeg absent | 503 on video path | Install correct binary with `libx264` |
| Browser MP4 cannot play | player duration 0 / console media error | Inspect codec, H.264 faststart, endpoint Content-Type, reload |
| Storage full | missing artifacts/write errors | Free disk; avoid deleting research source blindly |
| Codec timeout | server error, no completed record expected | Reduce video size; inspect FFmpeg stderr and resource contention |
| Potential jam signals inaccurate | stable conveyor bbox triggers | Treat as heuristic, review human annotations; no machinery intervention |

## Before production deployment

Introduce threat model, authn/authz, HTTPS, CORS hardening, rate limits, upload malware screening and content sniffing, quotas, queue and timeouts, durable storage, audit logging, observability, deployment tests, human override, incident response and legal review. **No production deployment instructions are endorsed without those gates.**
