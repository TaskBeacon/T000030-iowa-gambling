# Task Plot Review

## Evidence Match

- Pass: title and construct match the Iowa Gambling Task.
- Pass: rows reflect disadvantageous A/B decks, advantageous C/D decks, and timeout/no-draw behavior.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Decision -> Feedback -> ITI.
- Pass: timing labels match config: 300-500 ms fixation, 3500 ms decision, 1100 ms feedback, 300-600 ms ITI.
- Pass: decision mapping shows D=A, F=B, J=C, and K=D.
- Pass: feedback shows chosen deck, gain, loss, net outcome, and total score, with timeout shown as no draw and unchanged total.
- Pass: no extra betting phase, probability cue, or cue-target reaction stage is shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
