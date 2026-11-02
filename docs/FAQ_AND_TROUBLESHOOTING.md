# Troubleshooting and Frequently Asked Questions

## First-aid diagnosis

**Video output shows `0:00`** — inspect `ffprobe` codec; OpenCV `mp4v` inside `.mp4` may fail in Edge/Chrome. Ensure `VideoWriter.release()` before H.264/`yuv420p`/`+faststart` conversion; serve the final file in `FileResponse` and reload UI. Verify `/api/v1/artifacts/…` returns `video/mp4` and nonzero bytes.

**CUDA False despite RTX GPU** — `nvidia-smi` shows driver, PyTorch wheel may be CPU-only. Check `torch.__version__`, `torch.version.cuda`, `torch.cuda.is_available()`. Use compatible official CUDA PyTorch wheels in the project's venv, not system Python. Do not uninstall packages globally.

**GPU OOM** — RTX 3050 Ti laptop has 4 GiB VRAM. Close heavy GPU workloads, shorten video, reduce resolution, retain batch 1; CPU fallback may help.

**Nothing in raw image/video folders** — those folders are user-supplied testing inputs. Annotated Kaggle previews cannot be unannotated by simply renaming. A script reading an empty folder exits silently unless it explicitly checks count. Download or record properly licensed original footage first.

**`git status` shows `??`** — untracked file, not an execution error. Verify ignore rules, and stage chosen paths only. Git ignore does not retroactively untrack files already committed.

**Model load fails** — `.pt` weights intentionally not in Git; confirm `models/champion/conveyorjam_champion.pt` and check Ultralytics/PyTorch compatibility.

**Unexpected potential jam events** — static conveyor geometry is not a measurement of moving material; tracker jitter and camera motion can fool centroid dwell. Do not call the event a jam without verified labeling.

**High source mAP vs weak real world performance** — source test was all positive with unknown independent video grouping. Domain change, missing negatives and near-duplicate video frames can inflate apparent performance.

**Does `DELETE /history` delete media?** No. It deletes SQLite rows, explicitly leaves artifact files.

**Can I market it as a factory safety system?** No. There is no independent real-jam ground truth, safety validation, fail-safe review or production deployment evidence.

**Can I publish dataset videos/weights?** Not until each original source license and third-party obligations have been verified; MIT project software license does not grant those rights.

**Does GPU loaded mean video pipeline works?** No. Model load on CUDA demonstrates compatibility; codec, browser display and result persistence require separate tests.

**How do I reproduce Kaggle metrics?** Obtain original source, notebook, dependencies, group audit and trained checkpoint as authorized; re-run and compare exact report JSON. Local `.pt`/raw videos are excluded from Git clone.

**Can I build real jam detection from this?** Yes as a future research direction, by defining material motion, collecting labeled jam/normal videos and evaluating time-localized fault labels on independent sites. That is not shipped functionality.
