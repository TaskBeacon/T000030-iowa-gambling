# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['free_choice']` | W2035258287 | IGT trials are modeled as repeated free choices among four decks rather than externally assigned conditions. | inferred | Deck identity is logged as trial outcome, not pre-assigned condition. |
| task.blocks | `task.total_blocks`, `task.trial_per_block` | Human: `2 x 50`; QA/sim: `1 x 20` | W2035258287 | Canonical IGT uses repeated choice history; 100-trial envelope is preserved in human mode. | inferred | QA/sim reduced only for faster validation runtime. |
| task.key_mapping | `task.deck_a_key..task.deck_d_key` | `d/f/j/k` | W2144547056 | Four stable response options are required for simultaneous deck selection. | inferred | Mapping remains configurable for localization or hardware constraints. |
| task.localization.deck_labels | `task.deck_labels` | `deck_a=A, deck_b=B, deck_c=C, deck_d=D` | W2035258287 | Participant-facing deck labels must stay config-defined for language portability. | inferred | Runtime passes `deck_label` to feedback template. |
| timing.fixation | `timing.fixation_duration` | Human `[0.3, 0.5]`; QA/sim `[0.12, 0.18]` | W2035258287 | Brief pre-decision fixation separates consecutive selections. | inferred | Trial-wise jitter sampled by controller. |
| timing.decision_deadline | `timing.decision_deadline` | Human `3.5s`; QA/sim `0.7s` | W2123110589 | Bounded response window is required for omission/RT monitoring. | inferred | Timeout branch logs no deck draw and emits timeout trigger. |
| timing.feedback | `timing.feedback_duration` | Human `1.1s`; QA/sim `0.12s` | W2123110589 | Immediate explicit outcome feedback is central to IGT learning behavior. | inferred | Same feedback structure across modes, shorter durations in QA/sim. |
| timing.iti | `timing.iti_duration` | Human `[0.3, 0.6]`; QA/sim `[0.08, 0.12]` | W2035258287 | Inter-trial interval jitter reduces rhythmic anticipation. | inferred | Sampled by controller each trial. |
| controller.initial_money | `controller.initial_money` | `2000` | W2035258287 | Session starts with a score bank to accumulate net outcomes across draws. | inferred | Used in summaries and trial feedback. |
| controller.deck_a_profile | `controller.deck_profiles.deck_a` | `gain=100`, repeating losses `[0,150,0,300,0,200,0,250,0,350]` | W2108913208 | Disadvantageous deck with high rewards and frequent penalties. | inferred | Repeating sequence makes deck schedule auditable. |
| controller.deck_b_profile | `controller.deck_profiles.deck_b` | `gain=100`, repeating losses `[0,0,0,0,0,0,0,0,0,1250]` | W2108913208 | Deck-B low-frequency large-loss signature is explicitly represented. | high | Preserves deck-B loss-frequency phenomenon. |
| controller.deck_c_profile | `controller.deck_profiles.deck_c` | `gain=50`, repeating losses `[0,25,0,50,0,25,0,75,0,75]` | W2035258287 | Advantageous deck with lower gain and lower long-run penalty. | inferred | Implemented as deterministic schedule. |
| controller.deck_d_profile | `controller.deck_profiles.deck_d` | `gain=50`, repeating losses `[0,0,0,0,0,0,0,0,0,250]` | W2035258287 | Advantageous deck with infrequent moderate losses. | inferred | Complements deck-C advantageous profile. |
| trigger.decision | `triggers.map.decision_onset` | `30` | W2144547056 | Choice-phase onset should be event-coded for synchronization. | inferred | Emitted at decision screen onset. |
| trigger.deck_choices | `triggers.map.choice_deck_a..choice_deck_d` | `31..34` | W2144547056 | Deck identity at response is behaviorally critical and should be separable. | inferred | Sent after response-key to deck mapping. |
| trigger.choice_timeout | `triggers.map.choice_timeout` | `35` | W2144547056 | Omission/no-response events require dedicated coding. | inferred | Emitted by capture timeout policy. |
| trigger.feedback_iti | `triggers.map.feedback_onset`, `triggers.map.iti_onset` | `40`, `50` | W2155857408 | Decision-outcome and inter-trial boundaries should be separable for analysis. | inferred | Used in all modes. |
