# Testing, Evidence and Reproduction Playbook

## Validation layers

| Layer | Test | Current evidence | Release expectation |
|---|---|---|---|
| Python syntax | `py_compile` | Local manual execution claimed, not CI record | Must pass |
| Backend API | `pytest backend/tests` | API and synthetic dwell tests exist | Run and record result |
| CUDA | `torch.cuda.is_available()` | Local RTX 3050 Ti confirmed CUDA 12.8 | Document CPU fallback |
| Detector | Labeled image split | Kaggle source held-out result | Repeat with known provenance |
| Video encoding | ffprobe + browser playback | Local FFmpeg H.264 conversion evidence | Add automated smoke test |
| Frontend build | `npm run build` | Build tool configured | Must pass |
| Jam classification | Event ground truth | **Not available** | Block jam accuracy claim |
| Security | Auth, media isolation, fuzzing | **Not verified** | Block public deployment |

## Local quick-check (Windows PowerShell)

```powershell
cd 'D:\porto\100 day\day 29\ConveyorJam Watch'
.\.venv\Scripts\python -m py_compile backend\app\main.py
.\.venv\Scripts\python -m pytest backend\tests -q
.\.venv\Scripts\python -m pip check
.\.venv\Scripts\python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
ffmpeg -version
cd frontend
npm ci
npm run build
```

## Browser playback smoke test

1. Start backend; upload a licensed unannotated short conveyor MP4.
2. Confirm API returns one existing `.mp4` URL and history row.
3. Run `ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt,width,height -show_entries format=duration -of json <output.mp4>`; expect h264, yuv420p and positive duration.
4. Open result in Edge/Chrome with a clean page reload; verify seeks and playback.
5. Try malformed input, oversized upload, unsupported file, unavailable CUDA, missing FFmpeg.
6. Verify no staging/intermediate files remain on failed request and inspect logs.

## Full training reproduction

1. Obtain authorized source dataset and record license, data version and checksums.
2. Inspect `notebooks/conveyorjam-watch.ipynb`; verify no hand-authored output substituted for execution.
3. Validate source train/valid/test inventories and absence of exact duplicates; investigate temporal leakage separately.
4. Reproduce both detector experiments with seed 42 and the recorded optimizer/hyperparameters (read notebook for exact settings).
5. Select champion with validation **only**; evaluate original test once.
6. Export model, source audit, environment and metric JSON; record GPU, software and data hashes.
7. For external generalization reserve new camera/video/site test data before trying models.

Do not claim same-result reproducibility merely because JSON copies exist; a cloned repo intentionally does not ship data or weights.

## Definition of done

A change is complete only with: scope documented, reproducible instructions, relevant tests passed, no new unverified research assertions, no secrets, and no accidental large binary commits. Update source-of-truth documents when changing API, data layout, metrics or release boundary.
