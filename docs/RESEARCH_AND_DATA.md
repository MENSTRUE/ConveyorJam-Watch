# Research, Dataset and Model Evidence — ConveyorJam Watch

**Status:** executed detector study; **no jam-event ground truth**. Last documentation audit 2026-11-02.

## 1. Study identity

- Research objective: assess single-class conveyor bounding-box detection and integrate tracking/temporal rule demonstration.
- Primary executable data root: `/kaggle/input/datasets/loliwibu/conveyorjam-dataset`.
- Iron ore YOLO data: `iron-ore/yolo-dataset-center`, with `data.yaml` class index `0: conveyor`.
- Seed: 42. Original split supplied by source dataset; source-video independence not verified.
- Evidence master: `reports/research/research_report.json`.

## 2. Source and evidence inventory

| Item | Purpose | Current evidence location | Licensing |
|---|---|---|---|
| Iron Ore Conveyor | Detector fitting and source-image evaluation | `reports/audit/source_provenance.csv` | NOT_VERIFIED |
| Supervisely conveyor video | Auxiliary tracking demo | `reports/audit/video_inventory.csv` | NOT_VERIFIED |
| Camera-Based Conveyor Inspection Tracking | Reference | `reports/audit/source_provenance.csv` | NOT_VERIFIED |
| Additional local unannotated footage | App smoke testing | `assets/examples/raw_videos/` locally if available | Per-media verification required |

A future provenance amendment must provide source URL, exact version or checksum, license URL and terms, acquisition date, derivation recipe, intended permitted uses, and redistribution permission; missing provenance is **not** permission.

## 3. Data and split facts

| Split | Images | Positive | Negative | Boxes |
|---|---:|---:|---:|---:|
| Train | 2283 | 2283 | 0 | 2283 |
| Valid | 96 | 96 | 0 | 96 |
| Test | 95 | 95 | 0 | 95 |

Audited exact SHA cross-split duplicate groups: **0 detected**. Audited same-origin filename-stem groups: **0 detected**. The audit cannot show adjacent video frames have no visual similarity or that origin video groups are unique across splits. It is scientifically invalid to call the split independently sampled from these checks alone.

Review `reports/audit/annotation_errors.csv`, `orphan_labels.csv`, pair manifests, `sha_cross_split_audit.json`, and `original_stem_overlap.json` when re-running.

## 4. Actual detector evaluation

| Model | Val mAP50:95 | Val mAP50 | Val P | Val R |
|---|---:|---:|---:|---:|
| YOLOv8n | 0.98953125 | 0.995 | 0.99944172 | 1.0 |
| YOLOv8s | **0.9905239143** | 0.995 | 0.99945005 | 1.0 |

Champion: YOLOv8s chosen by validation mAP50:95. Held-out source test: **95 images**, **mAP50 = 0.995**, **mAP50:95 = 0.9847654346**, **P=1.0**, **R=1.0**. Do not substitute these metrics into jam event classification.

## 5. Qualitative demonstration evidence

- COCO pretrained tracking demo: `tracking_conveyor_annotated.mp4`; 500 processed frames, approx 25.26 measured processing FPS, 0 potential flags. Domain/class may differ from fine-tuned detector.
- Fine-tuned iron ore video 1: 980 processed frames, approx 43.45 measured processing FPS, 1 candidate flag.
- Fine-tuned iron ore video 2: 998 processed frames, approx 41.88 measured processing FPS, 1 candidate flag.
- Candidate flags total **2**, unverified. Source: `reports/video_analysis/potential_jam_events_UNVERIFIED.csv`.
- Synthetic dwell scenarios `moving`, `brief_stop`, `long_stop` met expected outputs, but do not form a real-event confusion matrix.

## 6. Methodological risks and corrective protocol

1. **Positive-only data:** source test does not characterize conveyor-absent false positives.
2. **Correlated frames:** need video/site grouping and visual near-duplicate analysis.
3. **Class semantics:** static bbox is not belt/material speed. Add optical flow or material-object tracking as a new separately evaluated model.
4. **Annotation coverage:** obtain independent jam, normal, stopped, empty-belt, blockage, blur and camera-motion sequences with start/end times, adjudication and confidence.
5. **External test:** reserve new camera/site groups **before** training; disclose uncertainty and per-site metrics.
6. **Baseline comparison:** report detector and event detection separately. Event metrics must include defined true/false positive and time windows.
7. **Independent replication:** retain train configuration, environment, source hashes, best epoch, model card and outputs.

## 7. Reproduction acceptance

Reproduction is not achieved by replaying a saved JSON. It requires original authorized data, notebook, exact split, dependencies, training, validation-only selection, and independent test output. A repository clone excludes weights and original videos. `notebooks/conveyorjam-watch.ipynb` must be available locally or from the saved Kaggle version to rerun the original training. Do not invent a Kaggle URL if its exact notebook version isn't recorded.

## 8. Claim language

Use: “conveyor localization, tracking and **unverified low-motion flags**.” Avoid: “accurate jam detection,” “reliable anomaly detection,” “production-ready,” “safety-certified,” or “no false positives.” See `reports/research/claim_boundaries.json`.
