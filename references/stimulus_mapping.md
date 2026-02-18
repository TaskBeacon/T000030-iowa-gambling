# Stimulus Mapping

Task: `Iowa Gambling Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `deck_a` | `deck_a_cue`, `deck_a_target` | `W2109668460` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for DECK A; target token for condition-specific response context. |
| `deck_b` | `deck_b_cue`, `deck_b_target` | `W2109668460` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for DECK B; target token for condition-specific response context. |
| `deck_c` | `deck_c_cue`, `deck_c_target` | `W2109668460` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for DECK C; target token for condition-specific response context. |
| `deck_d` | `deck_d_cue`, `deck_d_target` | `W2109668460` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for DECK D; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
