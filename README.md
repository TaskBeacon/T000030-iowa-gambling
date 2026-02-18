# Iowa Gambling Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Iowa Gambling Task |
| Version | v0.1.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000030-iowa-gambling |
| Short Description | Affective decision making under uncertain reward/punishment contingencies. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-18 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | English |
| Voice Name |  |

## 1. Task Overview

This task implements an Iowa Gambling-style paradigm with four deck conditions: `deck_a`, `deck_b`, `deck_c`, and `deck_d`. Trials include cueing, anticipation, target response capture, and feedback.

The implementation supports standardized execution across human, QA, scripted sim, and sampler sim profiles, with condition-specific trigger mappings and trial logging.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Load condition stream | Block-level condition sequence is prepared from configured deck labels. |
| 2. Execute trial loop | `run_trial(...)` presents cue, anticipation, target, and feedback stages. |
| 3. Block summary | Accuracy and score summary is displayed after each block. |
| 4. Task completion | End-of-task cumulative score is displayed. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Deck-specific cue is shown. |
| Anticipation | Fixation period with response monitoring. |
| Target | Deck-specific target appears with response capture. |
| Pre-feedback fixation | Brief interstitial fixation stage. |
| Feedback | Hit/miss feedback and score delta are shown. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive target timing | Controller adapts target duration toward configured accuracy. |
| Deck history tracking | Outcomes are tracked separately per deck condition. |
| Score update | Trial hit/miss state updates score delta and running total. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `anticipation` | Pre-target monitoring interval. |
| `target` | Active target response window. |

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
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `deck_*_cue` | text | Deck cue prompts for A/B/C/D conditions. |
| `deck_*_target` | text | Deck target prompts for response capture. |
| `deck_*_hit_feedback`, `deck_*_miss_feedback` | text | Deck-specific feedback text. |
| `fixation`, `block_break`, `good_bye` | text | Shared fixation and summary screens. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive via controller (`0.08`-`0.40` s bounds) |

## 4. Methods (for academic publication)

Participants completed repeated deck-selection trials under uncertain outcome contingencies. Each trial provided a deck cue, response window, and immediate feedback to support analysis of preference patterns and performance over time.

Task difficulty was managed with adaptive target duration limits, and trial-level logs captured condition identity, response status, timing, and score changes.

Trigger events were emitted for cue, anticipation, target, response, and feedback stages to support synchronized behavioral and neurophysiological acquisition workflows.
