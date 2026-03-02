# Task Logic Audit: Iowa Gambling Task

## 1. Paradigm Intent

- Task: `iowa_gambling`.
- Construct: affective decision-making under uncertain reward/loss contingencies.
- Manipulated trial factor: participant chooses one of four decks (`A/B/C/D`) each trial.
- Primary dependent measures:
  - advantageous-deck rate (`C/D` among responded trials)
  - deck-wise selection counts
  - reaction time and timeout rate
  - cumulative and trial-wise net outcomes.
- Key citations:
  - `W2035258287` (Li et al., 2009, Human Brain Mapping)
  - `W2108913208` (Lin et al., 2007, Behavioral and Brain Functions)
  - `W2144547056` (Bolla et al., 2004, Cerebral Cortex)
  - `W2155857408` (Fellows, 2004, Cerebral Cortex)

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `2` blocks x `50` trials.
- QA/sim profiles: `1` block x `20` trials.
- Controller state:
  - `start_block(block_idx)` resets block metrics.
  - cumulative money is preserved across blocks.

### Trial State Machine

1. `fixation`
- Stimulus: `fixation`.
- Trigger: `fixation_onset`.
- Keys: none.

2. `decision`
- Stimuli: `decision_title`, `balance_text`, four deck cards (`deck_*_rect` + `deck_*_label`), `key_hint`.
- Trigger: `decision_onset`.
- Valid keys: configured deck keys (`deck_a_key`, `deck_b_key`, `deck_c_key`, `deck_d_key`).
- Response triggers: `choice_deck_a`, `choice_deck_b`, `choice_deck_c`, `choice_deck_d`.
- Timeout trigger: `choice_timeout`.

3. `feedback`
- Trigger: `feedback_onset`.
- Stimulus branch:
  - `feedback_outcome` when a deck was chosen.
  - `feedback_timeout` when decision timed out.
- Keys: none.

4. `iti`
- Stimulus: `fixation`.
- Trigger: `iti_onset`.
- Keys: none.

## 3. Condition Semantics

- Runtime condition ID: `free_choice`.
- Participant-facing meaning: every trial presents all four decks simultaneously for free selection.
- Deck semantics:
  - `deck_a` and `deck_b`: disadvantageous in long-run expected value.
  - `deck_c` and `deck_d`: advantageous in long-run expected value.
- Outcome semantics:
  - each non-timeout choice draws deterministic gain/loss from the chosen deck schedule.
  - timeout produces no draw and no score change.

## 4. Response and Scoring Rules

- Response mapping (default):
  - `d -> deck_a`
  - `f -> deck_b`
  - `j -> deck_c`
  - `k -> deck_d`
- Timeout policy:
  - no deck draw
  - `gain=0`, `loss=0`, `net=0`
  - timeout feedback screen.
- Score update policy:
  - `net = gain - loss`
  - `balance_after = balance_before + net`.
- Logged trial fields include:
  - `chosen_deck`, `response_key`, `timed_out`, `rt_s`
  - `gain`, `loss`, `net_outcome`
  - `balance_before`, `balance_after`
  - `advantageous_choice`, `draw_index`.

## 5. Stimulus Layout Plan

- Decision screen layout (`1280x720`, `pix`):
  - `decision_title` at top center (`0, 300`).
  - `balance_text` below title (`0, 245`).
  - four deck rectangles in one row:
    - A: `(-420, 10)`
    - B: `(-140, 10)`
    - C: `(140, 10)`
    - D: `(420, 10)`
  - deck labels centered on each card (`y=20`) with key hints.
  - `key_hint` near bottom (`0, -260`).
- Visual intent:
  - all choice options visible concurrently.
  - cumulative score remains visible during decision.
- Localization policy:
  - participant-facing strings and labels are defined in `config/*.yaml`, not hardcoded in runtime.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation onset |
| `decision_onset` | 30 | decision screen onset |
| `choice_deck_a` | 31 | chose deck A |
| `choice_deck_b` | 32 | chose deck B |
| `choice_deck_c` | 33 | chose deck C |
| `choice_deck_d` | 34 | chose deck D |
| `choice_timeout` | 35 | no response before deadline |
| `feedback_onset` | 40 | feedback onset |
| `iti_onset` | 50 | inter-trial interval onset |

## 7. Architecture Decisions (Auditability)

- `main.py` keeps one mode-aware execution path for `human|qa|sim`, with identical trial orchestration.
- `src/run_trial.py` uses IGT-native phases only (`fixation -> decision -> feedback -> iti`) and removes MID-template states.
- Deck response identity is encoded by explicit post-response trigger emission (`choice_deck_a..d`) after key-to-deck mapping.
- Trial context includes key mapping and balance factors, supporting responder simulation and reproducible QA traces.
- Controller-owned deck schedules are deterministic and auditable (`draw_index` logged per trial).

## 8. Inference Log

- Exact human-mode durations (fixation and ITI jitter ranges, decision deadline) are implementation inferences constrained by IGT behavioral workflow rather than fixed citation-mandated constants.
- Splitting 100 human trials into `2 x 50` blocks is an operational inference for pacing while preserving total exposure.
- Deck labels are config-defined (`A/B/C/D`) to satisfy localization portability; symbolic labels are not forced by cited papers but are required for clear participant instructions.
- QA and simulation use shortened timing and fewer trials as validation-oriented inferences and do not alter core task-state semantics.
