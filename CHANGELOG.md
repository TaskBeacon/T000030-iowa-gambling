# CHANGELOG

## [v0.1.3-dev] - 2026-03-02

### Changed
- Replaced `src/run_trial.py` MID-template flow with Iowa Gambling native phases (`fixation -> decision -> feedback -> iti`).
- Implemented deck-choice execution using controller deck schedules (`draw_from_deck`) and explicit timeout no-draw behavior.
- Added config-first localization field `task.deck_labels` across all runtime profiles and used it for participant-facing feedback deck labels.
- Rebuilt references artifacts to the new contract format:
  - `references/references.yaml`
  - `references/references.md`
  - `references/parameter_mapping.md`
  - `references/stimulus_mapping.md`
  - `references/task_logic_audit.md`

### Fixed
- Removed leftover MID states (`cue`, `anticipation`, `target`, prefeedback fixation) from IGT trial runtime.
- Fixed trial ID progression by using controller-driven trial indexing.
- Restored reference-contract compliance (required headings, required table columns, required audit sections `## 7` and `## 8`).

## [v0.1.2-dev] - 2026-02-19

### Changed
- Rebuilt `T000030` from MID-style cue/target scaffold into a true Iowa Gambling Task with free deck choice each trial.
- Replaced adaptive hit/miss controller with deck-outcome controller using deck-specific gain/loss schedules and cumulative score updates.
- Rewrote trial runtime to `fixation -> decision -> feedback -> iti` with deck-specific response triggers and timeout handling.
- Replaced all config files with clean UTF-8 Chinese participant-facing stimuli and explicit four-deck card layout.
- Reworked sampler responder to multi-key deck-choice sampling (`A/B/C/D`) with configurable timeout rate.
- Rebuilt evidence artifacts (`task_logic_audit.md`, `stimulus_mapping.md`, `parameter_mapping.md`, `references.*`, `selected_papers.json`) to literature-first IGT logic.
- Synced metadata (`README.md`, `taskbeacon.yaml`) to repaired implementation.

### Fixed
- Removed placeholder/MID participant stimuli and deprecated cue/target feedback semantics.
- Removed mojibake/corrupted Chinese strings from task configs.

## [v0.1.1-dev] - 2026-02-19

### Changed
- Rebuilt literature bundle with task-relevant curated papers and regenerated reference artifacts.
- Replaced corrupted `references/task_logic_audit.md` with a full state-machine audit.
- Updated `references/stimulus_mapping.md` to concrete implemented stimulus IDs per condition.
- Synced metadata (`README.md`, `taskbeacon.yaml`) with current configuration and evidence.

All notable development changes for `T000030-iowa-gambling` are documented here.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Iowa Gambling Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
