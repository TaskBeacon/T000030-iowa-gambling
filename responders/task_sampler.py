from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for Iowa Gambling deck-choice trials."""

    deck_a_rate: float = 0.22
    deck_b_rate: float = 0.22
    deck_c_rate: float = 0.28
    deck_d_rate: float = 0.28
    miss_rate: float = 0.1
    rt_mean_s: float = 0.7
    rt_sd_s: float = 0.12
    rt_min_s: float = 0.2

    def __post_init__(self) -> None:
        self._rng: Any = None
        probs = [float(self.deck_a_rate), float(self.deck_b_rate), float(self.deck_c_rate), float(self.deck_d_rate)]
        probs = [max(0.0, p) for p in probs]
        total = sum(probs)
        if total <= 0:
            probs = [0.25, 0.25, 0.25, 0.25]
            total = 1.0

        self.deck_a_rate = probs[0] / total
        self.deck_b_rate = probs[1] / total
        self.deck_c_rate = probs[2] / total
        self.deck_d_rate = probs[3] / total

        self.miss_rate = max(0.0, min(1.0, float(self.miss_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _weighted_deck(self) -> str:
        r = self._sample_random()
        cuts = [
            self.deck_a_rate,
            self.deck_a_rate + self.deck_b_rate,
            self.deck_a_rate + self.deck_b_rate + self.deck_c_rate,
            1.0,
        ]
        if r < cuts[0]:
            return "deck_a"
        if r < cuts[1]:
            return "deck_b"
        if r < cuts[2]:
            return "deck_c"
        return "deck_d"

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        rng = self._rng
        if rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        phase = str(obs.phase or "")
        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))

        if phase != "decision":
            key = "space" if "space" in valid_keys else valid_keys[0]
            return Action(key=key, rt_s=rt, meta={"source": "task_sampler", "phase": phase, "outcome": "continue"})

        if self._sample_random() < self.miss_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "timeout"})

        factors = dict(obs.task_factors or {})
        deck_to_key = {
            "deck_a": str(factors.get("deck_a_key", "")).strip().lower(),
            "deck_b": str(factors.get("deck_b_key", "")).strip().lower(),
            "deck_c": str(factors.get("deck_c_key", "")).strip().lower(),
            "deck_d": str(factors.get("deck_d_key", "")).strip().lower(),
        }

        for deck, key in list(deck_to_key.items()):
            if key not in valid_keys:
                deck_to_key[deck] = ""

        for idx, deck in enumerate(("deck_a", "deck_b", "deck_c", "deck_d")):
            if not deck_to_key[deck]:
                if idx < len(valid_keys):
                    deck_to_key[deck] = valid_keys[idx]
                else:
                    deck_to_key[deck] = valid_keys[-1]

        deck = self._weighted_deck()
        key = deck_to_key.get(deck, valid_keys[0])
        return Action(
            key=key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "outcome": "choose_deck",
                "deck": deck,
            },
        )
