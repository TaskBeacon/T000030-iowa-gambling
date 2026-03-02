# Iowa Gambling Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Iowa Gambling Task |
| Version | v0.1.2-dev |
| URL / Repository | https://github.com/TaskBeacon/T000030-iowa-gambling |
| Short Description | Four-deck decision task probing long-term reward/loss learning under uncertainty. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements the Iowa Gambling Task (IGT) with four visible decks (`A/B/C/D`). On each trial, participants choose one deck and immediately receive gain/loss feedback. Long-term deck contingencies are configured so that `A/B` are disadvantageous and `C/D` are advantageous across repeated choices.

The implementation records trial-level choice, gain/loss values, net outcome, cumulative score, timeout status, and response latency.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block init | Controller resets block metrics and keeps cumulative score continuity. |
| 2. Trial loop | Each trial presents all four decks for free choice and logs outcome updates. |
| 3. Block summary | Show current total score, net change, advantageous choice rate, RT, and deck counts. |
| 4. Final summary | Show full-session totals and deck-selection profile. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `fixation` | Jittered fixation before deck decision. |
| `decision` | Show four deck cards and capture key response (`D/F/J/K`). |
| `feedback` | Show chosen deck, gain, loss, net outcome, and updated total (or timeout message). |
| `iti` | Jittered inter-trial fixation before next choice. |

### Controller Logic

| Component | Description |
|---|---|
| Deck schedules | Each deck has fixed gain and repeating loss sequence (`deck_profiles`). |
| Score update | Per trial: `net = gain - loss`; cumulative total is updated online. |
| Metrics | Tracks timeout rate, advantageous choice rate (`C/D`), deck counts, and RT summaries. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `fixation` | Pre-choice baseline display. |
| `decision` | Active free-choice window among four decks. |
| `feedback` | Outcome display after choice (or timeout). |
| `iti` | Inter-trial reset interval. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `[0.07, 0.1, 0.14]` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus Group | Description |
|---|---|
| `deck_*_rect`, `deck_*_label` | Four deck cards with fixed spatial layout and key labels. |
| `decision_title`, `balance_text`, `key_hint` | Decision header and current score display. |
| `feedback_outcome`, `feedback_timeout` | Outcome-specific feedback panels. |
| `instruction_text`, `block_break`, `good_bye`, `fixation` | Shared envelope and transition screens. |

### d. Timing

| Stage | Duration |
|---|---|
| fixation | jittered (`fixation_duration`) |
| decision | fixed deadline (`decision_deadline`) |
| feedback | fixed (`feedback_duration`) |
| iti | jittered (`iti_duration`) |

### e. Triggers

| Trigger | Code |
|---|---:|
| `exp_onset` | 1 |
| `exp_end` | 2 |
| `block_onset` | 10 |
| `block_end` | 11 |
| `fixation_onset` | 20 |
| `decision_onset` | 30 |
| `choice_deck_a` | 31 |
| `choice_deck_b` | 32 |
| `choice_deck_c` | 33 |
| `choice_deck_d` | 34 |
| `choice_timeout` | 35 |
| `feedback_onset` | 40 |
| `iti_onset` | 50 |

### f. Adaptive Controller

| Parameter Group | Description |
|---|---|
| `deck_profiles` | Deck-specific gain and loss schedules (`A/B` disadvantageous, `C/D` advantageous). |
| `initial_money` | Initial cumulative score baseline. |
| `enable_logging` | Emits per-trial controller logs for QA/debug analysis. |

## 4. Methods (for academic publication)

Participants completed repeated uncertain-choice trials in a four-deck Iowa Gambling paradigm. On each trial they selected one deck using a fixed four-key mapping and received immediate gain/loss outcome feedback. Deck contingencies were configured to dissociate short-term reward magnitude from long-term expected value, enabling quantification of advantageous-deck preference over time.

The task records trial-level deck choice, gain/loss/net values, cumulative score, reaction time, and timeout events with trigger-aligned phase labels (`fixation`, `decision`, `feedback`, `iti`) for reproducible behavioral and multimodal synchronization workflows.
