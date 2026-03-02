# Stimulus Mapping

Task: `Iowa Gambling Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `free_choice` | `decision_title`, `balance_text`, `deck_a_rect`, `deck_b_rect`, `deck_c_rect`, `deck_d_rect`, `deck_a_label`, `deck_b_label`, `deck_c_label`, `deck_d_label`, `key_hint`, `feedback_outcome`, `feedback_timeout`, `fixation` | `W2035258287` | IGT is implemented as repeated free choices among four decks with trial-wise feedback. | `psychopy_builtin` | Decks are concurrently shown each trial; no pre-cue of a single deck is shown. |
| `deck_outcome_logic` | `feedback_outcome` (formatted gain/loss/net/total) | `W2108913208` | Deck-specific payoff structure (including deck-B loss-frequency profile) informs outcome schedules. | `psychopy_builtin` | Controller applies deck schedules and feeds formatted outcome text. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye` | `W2144547056` | Shared envelope screens support block progression and summary reporting in standard IGT sessions. | `psychopy_builtin` | Text remains Chinese and mode-consistent across human/QA/sim runs. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
