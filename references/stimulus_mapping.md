# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `free_choice` | fixation | `fixation` | Central `+` before each deck decision. | W2035258287 | Repeated trial envelopes include a brief pre-choice fixation period. | psychopy_builtin | `config/*.yaml -> stimuli.fixation` | Jittered duration sampled from controller settings. |
| `free_choice` | decision | `decision_title`, `balance_text`, `deck_a_rect`, `deck_b_rect`, `deck_c_rect`, `deck_d_rect`, `deck_a_label`, `deck_b_label`, `deck_c_label`, `deck_d_label`, `key_hint` | Four decks are shown concurrently; participant chooses one deck with configured keys. | W2035258287 | IGT behavior is defined by repeated free deck choice under uncertainty. | psychopy_builtin | `config/*.yaml -> stimuli.decision_* / deck_* / key_hint` | All participant wording and labels remain in config for localization. |
| `free_choice` | feedback | `feedback_outcome` | If a deck is chosen: show deck label, gain, loss, net, and updated balance. | W2108913208 | Deck-specific outcomes and cumulative consequences drive learning effects. | psychopy_builtin | `config/*.yaml -> stimuli.feedback_outcome` | Runtime formats values from controller draw result. |
| `free_choice` | feedback | `feedback_timeout` | If no response: show timeout message and unchanged balance. | W2123110589 | Omission handling is needed for RT/quality analysis in bounded decision windows. | psychopy_builtin | `config/*.yaml -> stimuli.feedback_timeout` | Timeout branch does not draw from any deck. |
| `free_choice` | iti | `fixation` | Brief fixation between trials. | W2035258287 | Inter-trial reset interval separates consecutive decision events. | psychopy_builtin | `config/*.yaml -> stimuli.fixation` | Triggered by `iti_onset`. |
| `all_conditions` | envelope | `instruction_text`, `block_break`, `good_bye` | Task instruction and summary screens with score and deck-choice metrics. | W2144547056 | Block/session summaries support interpretable progression of decision behavior. | psychopy_builtin | `config/*.yaml -> stimuli.instruction_text/block_break/good_bye` | No participant-facing trial text is hardcoded in `run_trial.py`. |
