# Dataset Provenance, License Ledger and Responsible Distribution

## Actual source inventory

| Source named in audit | Role | Status | Verification needed |
|---|---|---|---|
| Iron Ore Conveyor | Detector training and industrial video evaluation | `license=NOT_VERIFIED` | Original license URL, version, redistribution and commercial-use permission |
| Supervisely conveyor video | Tracking demonstration; possible other semantic classes | `license=NOT_VERIFIED` | Exact source/license and video reuse rights |
| Camera-Based Conveyor Inspection Tracking | Reference implementation/output | `license=NOT_VERIFIED` | Code and imagery rights independently |
| Local third-party stock video (if provided) | UI smoke testing | Media-specific license unrecorded | Save URL, license date, attribution and permitted use |

The name of a dataset does **not** establish its current license. Audit source: `reports/audit/source_provenance.csv`. Never replace `NOT_VERIFIED` with a presumed Creative Commons or public-domain license.

## Expected provenance fields

For every redistributed or trained-on asset: origin URL, author, version/commit, access UTC date, license name and URL, terms snapshot, image/video identity, checksum, transformations, split group, restrictions, consent/privacy notes if people appear, and redistribution decision with reviewer/date.

## Terms by artifact

- `LICENSE`: MIT for the author's original repository software and original documentation where applicable.
- Dataset media and labels: retain upstream rights; **MIT does not relicense them**.
- Ultralytics/package binaries: check their current licenses and commercial terms separately.
- Checkpoint: trained weights may inherit training-data and upstream software obligations; cannot assume freely redistributable.
- Screenshots and user-uploaded media: may include proprietary, identifying or sensitive operational data; keep private by default.

## Publishing gates

Before public demo/media/checkpoint release: verify distribution permissions, remove copyrighted source video if uncertain, anonymize sensitive content, disclose provenance and external model terms. Repository already contains some research screenshots and preview images; review their source licensing rather than assuming commit implies permission. Purge from Git history only with deliberate approval because rewrite affects collaborators.

## Data-quality limits

Reported images: train 2,283, validation 96, test 95, all positive conveyor examples; absence-of-conveyor negatives not represented. Exact-hash duplicate audit 0 and stem-overlap audit 0 do not rule out adjacent frames, same scene, compression edits or shared camera sites. Source-data split provenance requires independent video group IDs.
