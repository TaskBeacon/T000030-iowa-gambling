# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['free_choice']` | `W2035258287` | `high` | IGT trial logic is free deck choice, not externally cued deck condition. |
| `task.total_blocks` | `2` | `W2035258287` | `inferred` | Split blocks support operator pacing while preserving cumulative learning trajectory. |
| `task.trial_per_block` | `50` | `W2035258287` | `inferred` | 100 total choices implemented as 2 x 50 for standard IGT-scale sampling. |
| `task.deck_a_key` | `d` | `W2144547056` | `inferred` | Stable four-key mapping for four deck options. |
| `task.deck_b_key` | `f` | `W2144547056` | `inferred` | Stable four-key mapping for four deck options. |
| `task.deck_c_key` | `j` | `W2144547056` | `inferred` | Stable four-key mapping for four deck options. |
| `task.deck_d_key` | `k` | `W2144547056` | `inferred` | Stable four-key mapping for four deck options. |
| `timing.fixation_duration` | `[0.3, 0.5]` | `W2035258287` | `inferred` | Short jittered fixation to separate consecutive choices. |
| `timing.decision_deadline` | `3.5` | `W2123110589` | `inferred` | Bounded response window for consistent timeout and RT collection. |
| `timing.feedback_duration` | `1.1` | `W2123110589` | `inferred` | Explicit post-choice outcome display window. |
| `timing.iti_duration` | `[0.3, 0.6]` | `W2035258287` | `inferred` | Jittered ITI reduces rhythmic anticipation. |
| `controller.initial_money` | `2000` | `W2035258287` | `inferred` | Conventional baseline score bank for cumulative-loss/gain feedback. |
| `controller.deck_profiles.deck_a` | `gain=100, high-frequency losses` | `W2108913208` | `inferred` | Implements disadvantageous high-frequency-penalty structure. |
| `controller.deck_profiles.deck_b` | `gain=100, low-frequency large losses` | `W2108913208` | `high` | Captures deck-B loss-frequency property discussed in deck-B analyses. |
| `controller.deck_profiles.deck_c` | `gain=50, low-magnitude frequent losses` | `W2035258287` | `inferred` | Implements advantageous lower-reward/lower-loss structure. |
| `controller.deck_profiles.deck_d` | `gain=50, infrequent moderate losses` | `W2035258287` | `inferred` | Implements advantageous low-frequency-penalty structure. |
| `triggers.map.decision_onset` | `30` | `W2144547056` | `inferred` | Marks deck-choice screen onset for synchronization. |
| `triggers.map.choice_deck_a..d` | `31..34` | `W2144547056` | `inferred` | Distinguishes deck-specific response events. |
| `triggers.map.choice_timeout` | `35` | `W2144547056` | `inferred` | Explicit no-response event for exclusion/quality checks. |
| `triggers.map.feedback_onset` | `40` | `W2155857408` | `inferred` | Marks outcome display onset for decision-outcome analysis. |
| `triggers.map.iti_onset` | `50` | `W2155857408` | `inferred` | Marks inter-trial interval onset. |
