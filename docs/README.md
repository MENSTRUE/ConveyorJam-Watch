# Documentation Hub — ConveyorJam Watch

This is the canonical index for all long-form Markdown documentation. Read root [`README.md`](../README.md) first and root [`AGENTS.md`](../AGENTS.md) before agent-assisted code changes.

## Files shipped in the complete pack

| Path | Purpose |
|---|---|
| `README.md` | Full project entry point, source-of-truth, Before–Now–Next, evidence, setup, risks, roadmap |
| `AGENTS.md` | Mandatory implementation and research guardrails |
| `backend/README.md` | Runtime/API internals and backend troubleshooting |
| `frontend/README.md` | UI routes, operation, build and error-state acceptance |
| `docs/README.md` | This documentation map |
| `docs/ARCHITECTURE.md` | End-to-end system and contracts |
| `docs/RESEARCH_AND_DATA.md` | Audited data and experiments |
| `docs/DATASET_PROVENANCE_AND_LICENSES.md` | Source-by-source rights and provenance gaps |
| `docs/API_AND_OPERATIONS.md` | API examples and operating parameters |
| `docs/TESTING_AND_REPRODUCIBILITY.md` | Tests and experiment reproduction |
| `docs/QUALITY_SECURITY_DEPLOYMENT.md` | Quality/security and launch blockers |
| `docs/DEPLOYMENT_RUNBOOK.md` | Local operation and safe rollout boundary |
| `docs/ROADMAP_AND_FAQ.md` | Milestones, priorities and FAQ |
| `docs/FAQ_AND_TROUBLESHOOTING.md` | Common errors and recovery |
| `docs/CONTRIBUTING.md` | PR requirements and change workflow |
| `docs/research/KAGGLE_OUTPUT_README.md` | Original executed Kaggle results and caveats |
| `docs/id/README.md` | Indonesian guide |
| `docs/en/README.md` | English topic index |

## Evidence hierarchy

Executed JSON/CSV audits > actual checked-in implementation > local checkpoint/notebook if available > local smoke-test observations > documentation > roadmap. **Never invent an experiment, license, dataset split or safety validation.** No real jam ground truth exists yet.

## Document maintenance

- Backend route/config change: update `backend/README.md`, `docs/API_AND_OPERATIONS.md`, relevant section of root README.
- UI behavior change: update `frontend/README.md` and screenshot evidence if appropriate.
- Data/model rerun: update raw reports, then `docs/RESEARCH_AND_DATA.md`, provenance file, root metrics; preserve original runs.
- Security/public hosting change: update deployment runbook and security gates; require review.
- New documentation file: link it here and in appropriate language index.
