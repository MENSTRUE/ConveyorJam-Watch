# Before / Now / Next — Detailed Roadmap and Decision Log

## Before

- Target: a manufacturing-oriented computer-vision portfolio experiment rather than a generic web-only demo.
- Collected Iron Ore conveyor YOLO image data plus auxiliary conveyor tracking demos.
- Audited image/label pairing, exact cross-split hashes, image name overlaps and source manifests.
- Crucial data gap found: **all labeled detector images are positive conveyor examples; no annotated physical jams**.

## Now — evidence-backed

1. YOLOv8n and YOLOv8s trained/compared; YOLOv8s selected by source validation mAP50:95.
2. Source held-out test: 95 images, mAP50:95 = **0.9847654346**; cross-video independence unknown.
3. Three Kaggle video demonstration outputs and two **unverified** candidate flags.
4. React/FastAPI dashboard with upload, CPU/GPU choice, archive, research and monitor settings.
5. Local CUDA PyTorch successfully loaded the model on an RTX 3050 Ti; one 16-second video pipeline demo observed 161 detection observations.
6. FFmpeg H.264 conversion now exists in backend source. Full browser regression still a test gate.
7. Security, privacy, accurate physical jam semantics and dataset redistribution rights remain open.

## Next — milestone table

| Milestone | Minimum artifact | Validation criterion |
|---|---|---|
| M1 Repo hygiene | Reviewed Git commit | No runtime `.sqlite3`, local backup, raw video or checkpoint newly tracked |
| M2 Codec reliability | H.264 output integration test | Successful `ffprobe`, artifact endpoint 200, browser seek/play |
| M3 Dataset provenance | Updated audited CSV | Each source exact URL, license text, version/date, transformation rights |
| M4 Independent raw media | New external-site sequences | No source-video overlap and rights verified |
| M5 Jam annotation protocol | `jam_event_schema.md` + labeled cases | Adjudicated physical event types and timestamps, inter-annotator check |
| M6 Belt/material motion baseline | Optical-flow or product tracking experiment | Compared against static conveyor-bbox heuristic on event labels |
| M7 Calibrated detection | Validation/event report | Per-source false alarms, misses, latency and confidence |
| M8 Secure multi-user application | Auth/RBAC + durable settings | Automated functional/security tests |
| M9 Operational readiness | Async jobs, monitoring, retention | Load test, recovery runbooks and documented SLAs |
| M10 Authorized pilot | Field study and risk review | Explicit site owner approval and human oversight |

## Open research questions

- How should a jam be distinguished from a deliberately stopped machine, unloaded belt, slow movement, operator maintenance or emergency stop?
- Is belt-surface optical flow useful in low-texture scenes? Can structured light/physical speed sensors improve confidence?
- How many distinct camera sources are required for robust generalization, and how will negative-only scenes be included?
- How should alert debouncing, duration, operating mode and human acknowledgement be calibrated?
- What data retention and consent conditions apply to shop-floor video with workers?

## FAQ for maintainers

**Why is a visually stationary box not enough?** The conveyor structure is fixed to the factory, while its moving belt and material are internal. Tracking a fixed bounding box is not belt-motion sensing.

**Why not announce 99% jam accuracy?** The number comes from a *different task* — conveyor box localization — on a particular source image split.

**Why is the champion not in GitHub?** `.gitignore` excludes `.pt`; include a verified authorized artifact acquisition workflow and checksum in future releases.

**Can we run on NVIDIA laptop GPU?** Yes if CUDA-enabled PyTorch and compatible drivers are installed; 4-GB VRAM may limit resolution and concurrency.

**How to get demos?** Use authorized unannotated footage in `assets/examples/raw_videos/` or an independent source; existing annotated demonstrations are evidence, not untouched inputs.

**What remains urgent?** First repository data/backup cleanup and video playback regression, then independent physical-jam labels. More model complexity alone cannot fill an absent label definition.
