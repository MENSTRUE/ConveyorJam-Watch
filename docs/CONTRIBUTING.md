# Contributing and Agent Workflow

Read [AGENTS.md](../AGENTS.md) before opening a PR; it contains binding project boundaries. Use small, explainable commits and include tests/evidence. The repo is a research **conveyor detector plus unverified heuristic signal**, not a validated jam detector.

## Workflow

1. Open issue with scope, reproducible steps, expected behavior, evidence path and acceptance criteria.
2. Inspect code and current outputs before editing. Do not invent files or report new metrics without runs.
3. Create branch (`feat/...`, `fix/...`, `docs/...`, `test/...`), stage **named paths**, review `git diff --cached`.
4. Run Python compile and pytest when backend changes; `npm run build` for frontend; use actual clean raw-media browser smoke when codec changes.
5. Document public API/contracts and the research claim boundary if relevant.
6. PR must include Before–Now–Next, risk, tests, screenshots of actual changes if UI, rollback instructions.

## Commit examples

- `fix(video): transcode tracking previews to browser-playable H264`
- `test(api): add missing-ffmpeg and upload-limit cases`
- `docs: reconcile training metrics with executed reports`
- `chore(git): stop tracking runtime and backups`

## Data and model policy

No raw datasets directory in standard repository; do not commit `.pt`, `.mp4`, archives, `.env`, caches, local SQLite, user files, patch backups. Source media licensing is unresolved, so avoid redistribution. Prefer retaining report CSV/JSON with original measurements. If metrics differ, investigate first; do not adjust reports to match marketing language.

## Review priority

Correctness > scientific integrity > safety/privacy > reproducibility > clarity > cosmetics. Never remove a warning to make demos appear more successful. Fix broken browser playback as a media pipeline issue; do not suppress conversion errors.
