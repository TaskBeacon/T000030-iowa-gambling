# Stimulus Mapping

Task: `Iowa Gambling Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `deck_a` | `deck_a_cue`, `deck_a_target`, `deck_a_hit_feedback`, `deck_a_miss_feedback`, `fixation` | `W2035258287` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `deck_b` | `deck_b_cue`, `deck_b_target`, `deck_b_hit_feedback`, `deck_b_miss_feedback`, `fixation` | `W2035258287` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `deck_c` | `deck_c_cue`, `deck_c_target`, `deck_c_hit_feedback`, `deck_c_miss_feedback`, `fixation` | `W2035258287` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `deck_d` | `deck_d_cue`, `deck_d_target`, `deck_d_hit_feedback`, `deck_d_miss_feedback`, `fixation` | `W2035258287` | Condition-specific trial flow and outcome/response mapping described in selected paradigm references. | `psychopy_builtin` | Condition row resolved against current `config/config.yaml` stimuli and `src/run_trial.py` phase logic. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye`, `fixation` | `W2035258287` | Shared instruction, transition, and fixation assets support the common task envelope across all conditions. | `psychopy_builtin` | Shared assets are condition-agnostic and used in every run mode. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
