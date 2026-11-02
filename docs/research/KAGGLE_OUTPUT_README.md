# Kaggle Day 29 — Original executed research output

**Keep this document tied to the actual audit; do not rewrite past measurements to match future hypotheses.**

## Input and execution

- Kaggle data root: `/kaggle/input/datasets/loliwibu/conveyorjam-dataset`.
- Detection dataset: `iron-ore/yolo-dataset-center`; YOLO `data.yaml` with class `0: conveyor`.
- Source-provided splits: 2,283 train / 96 validation / 95 test, all positive and one bounding box per image in recorded audit.
- Study seed: 42; compared YOLOv8n and YOLOv8s, selected on validation mAP50:95.
- `reports/research/research_report.json` and `reports/evaluation/*` are authoritative for measured values. The notebook `notebooks/conveyorjam-watch.ipynb` and checkpoint `.pt` are **local** artifacts, not necessarily included in a GitHub clone.

## Metrics (detection only)

| Experiment | Validation mAP50:95 | Validation mAP50 |
|---|---:|---:|
| YOLOv8n | 0.98953125 | 0.995 |
| YOLOv8s | 0.9905239143 | 0.995 |

Champion YOLOv8s source test: 95 images, mAP50:95 0.9847654346, mAP50 0.995, precision 1.0 and recall 1.0. Exact-hash and original-name audits do not prove independent video-source splits. No negatives means absence-of-conveyor false alarms were not directly evaluated on this source split.

## Tracking demonstrations

Three annotated demonstration videos were exported locally; two potential low-motion events occurred in fine-tuned iron-ore footage, **no physical jam event adjudication**. `potential_jam_events_UNVERIFIED.csv` names these explicitly. One COCO-pretrained tracking video is a different detector/domain. Processing-FPS figures in the research report reflect their own recorded environment and are **not** local laptop FPS or promised live performance.

## License and sharing

`reports/audit/source_provenance.csv` records source licenses as `NOT_VERIFIED`. Do not represent this as licensed redistribution or place raw footage/checkpoints in GitHub before verifying upstream terms. Project code LICENSE is MIT, which does not automatically cover third-party data, annotations or pretrained weights.

## Directory guide

- `reports/audit/`: source manifests, duplicate audits, orphan/annotation checks, provenance.
- `reports/evaluation/`: model selection and held-out detector metrics.
- `reports/research/`: environment, claim boundaries and executed report.
- `reports/tests/`: synthetic dwell tests.
- `reports/video_analysis/`: sampled video analyses, events and timelines.
- `assets/examples/images/`: annotated preview images; **not unannotated test imagery**.
- `assets/examples/videos/`: annotated video outputs; intentionally Git-ignored.
- `assets/plots/`: timeline plots.
- `models/champion/`: local champion checkpoint, ignored by Git.
- `archives/`: local original ZIP, ignored by Git.

## Before–Now–Next

**Before:** assemble and audit iron-ore source data. **Now:** detection experiment and heuristic tracking demos executed. **Next:** acquire new video-disjoint, negative, jam-labeled evaluation data; extend to material motion; establish jam-event ground truth; quantify false-alert rate and time-to-detect. No production fault detection claim until independently measured.
