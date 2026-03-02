from __future__ import annotations

import random
from typing import Any

from psychopy import logging

DECK_A = "deck_a"
DECK_B = "deck_b"
DECK_C = "deck_c"
DECK_D = "deck_d"
ALL_DECKS = (DECK_A, DECK_B, DECK_C, DECK_D)
ADVANTAGEOUS_DECKS = {DECK_C, DECK_D}


class Controller:
    """Iowa Gambling Task controller with deterministic deck outcome schedules."""

    def __init__(
        self,
        fixation_duration: list[float] | tuple[float, ...] | float = (0.3, 0.5),
        decision_deadline: float = 3.5,
        feedback_duration: float = 1.1,
        iti_duration: list[float] | tuple[float, ...] | float = (0.3, 0.6),
        initial_money: int = 2000,
        deck_profiles: dict[str, Any] | None = None,
        random_seed: int | None = None,
        enable_logging: bool = True,
    ):
        self.fixation_duration = fixation_duration
        self.decision_deadline = max(0.2, float(decision_deadline))
        self.feedback_duration = max(0.1, float(feedback_duration))
        self.iti_duration = iti_duration
        self.initial_money = int(initial_money)
        self.enable_logging = bool(enable_logging)

        self.rng = random.Random(random_seed)
        self.deck_profiles = self._normalize_profiles(deck_profiles)

        self.total_money = int(self.initial_money)
        self.block_idx = -1
        self.trial_count_total = 0
        self.trial_count_block = 0

        self.deck_draw_counts = {deck: 0 for deck in ALL_DECKS}
        self.total_bucket = self._new_bucket()
        self.block_bucket = self._new_bucket()

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        cfg = dict(config or {})
        return cls(
            fixation_duration=cfg.get("fixation_duration", (0.3, 0.5)),
            decision_deadline=cfg.get("decision_deadline", 3.5),
            feedback_duration=cfg.get("feedback_duration", 1.1),
            iti_duration=cfg.get("iti_duration", (0.3, 0.6)),
            initial_money=cfg.get("initial_money", 2000),
            deck_profiles=cfg.get("deck_profiles", None),
            random_seed=cfg.get("random_seed", None),
            enable_logging=bool(cfg.get("enable_logging", True)),
        )

    @staticmethod
    def _default_profiles() -> dict[str, dict[str, Any]]:
        return {
            DECK_A: {
                "gain": 100,
                "loss_sequence": [0, 150, 0, 300, 0, 200, 0, 250, 0, 350],
            },
            DECK_B: {
                "gain": 100,
                "loss_sequence": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1250],
            },
            DECK_C: {
                "gain": 50,
                "loss_sequence": [0, 25, 0, 50, 0, 25, 0, 75, 0, 75],
            },
            DECK_D: {
                "gain": 50,
                "loss_sequence": [0, 0, 0, 0, 0, 0, 0, 0, 0, 250],
            },
        }

    @staticmethod
    def _normalize_losses(value: Any, fallback: list[int]) -> list[int]:
        if not isinstance(value, list):
            return list(fallback)
        out: list[int] = []
        for item in value:
            try:
                out.append(max(0, int(round(float(item)))))
            except Exception:
                continue
        return out or list(fallback)

    def _normalize_profiles(self, value: Any) -> dict[str, dict[str, Any]]:
        defaults = self._default_profiles()
        if not isinstance(value, dict):
            return defaults

        out: dict[str, dict[str, Any]] = {}
        for deck in ALL_DECKS:
            raw = value.get(deck, value.get(deck.upper(), {}))
            if not isinstance(raw, dict):
                raw = {}

            default_gain = int(defaults[deck]["gain"])
            default_losses = list(defaults[deck]["loss_sequence"])

            try:
                gain = int(round(float(raw.get("gain", default_gain))))
            except Exception:
                gain = default_gain

            losses = self._normalize_losses(raw.get("loss_sequence", default_losses), default_losses)
            out[deck] = {"gain": max(0, gain), "loss_sequence": losses}

        return out

    @staticmethod
    def _new_bucket() -> dict[str, Any]:
        return {
            "n": 0,
            "responses": 0,
            "timeouts": 0,
            "adv": 0,
            "rt_sum": 0.0,
            "rt_n": 0,
            "net_sum": 0,
            "gain_sum": 0,
            "loss_sum": 0,
            DECK_A: 0,
            DECK_B: 0,
            DECK_C: 0,
            DECK_D: 0,
        }

    @staticmethod
    def parse_condition(condition: str) -> str:
        token = str(condition).strip().lower()
        if token in {"", "free_choice", "igt", "trial"}:
            return "free_choice"
        return token

    def start_block(self, block_idx: int) -> None:
        self.block_idx = int(block_idx)
        self.trial_count_block = 0
        self.block_bucket = self._new_bucket()

    def next_trial_id(self) -> int:
        return int(self.trial_count_total) + 1

    def sample_duration(self, value: Any, default: float) -> float:
        if isinstance(value, (int, float)):
            return max(0.0, float(value))
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            try:
                low = float(value[0])
                high = float(value[1])
            except Exception:
                return max(0.0, float(default))
            if high < low:
                low, high = high, low
            return max(0.0, float(self.rng.uniform(low, high)))
        return max(0.0, float(default))

    def draw_from_deck(self, deck: str) -> dict[str, Any]:
        deck_id = str(deck).strip().lower()
        if deck_id not in self.deck_profiles:
            raise ValueError(f"Unsupported deck: {deck!r}")

        profile = dict(self.deck_profiles[deck_id])
        gain = int(profile.get("gain", 0))
        losses = list(profile.get("loss_sequence", [0]))
        if not losses:
            losses = [0]

        draw_index = int(self.deck_draw_counts[deck_id])
        loss = int(losses[draw_index % len(losses)])
        net = int(gain - loss)

        self.deck_draw_counts[deck_id] = draw_index + 1
        self.total_money += net

        return {
            "deck": deck_id,
            "draw_index": draw_index + 1,
            "gain": gain,
            "loss": loss,
            "net": net,
            "total_money": int(self.total_money),
        }

    def record_trial(
        self,
        *,
        deck: str | None,
        rt_s: float | None,
        timed_out: bool,
        gain: int,
        loss: int,
        net: int,
    ) -> None:
        self.trial_count_total += 1
        self.trial_count_block += 1

        deck_id = str(deck).strip().lower() if deck is not None else ""
        for bucket in (self.total_bucket, self.block_bucket):
            bucket["n"] += 1
            bucket["gain_sum"] += int(gain)
            bucket["loss_sum"] += int(loss)
            bucket["net_sum"] += int(net)

            if timed_out:
                bucket["timeouts"] += 1
            else:
                bucket["responses"] += 1

            if deck_id in ALL_DECKS:
                bucket[deck_id] += 1
                if deck_id in ADVANTAGEOUS_DECKS:
                    bucket["adv"] += 1

            if (rt_s is not None) and (not timed_out):
                rt = max(0.0, float(rt_s))
                bucket["rt_sum"] += rt
                bucket["rt_n"] += 1

        if self.enable_logging:
            logging.data(
                f"[IGT] block={self.block_idx} trial_block={self.trial_count_block} "
                f"trial_total={self.trial_count_total} deck={deck_id or 'none'} "
                f"timed_out={timed_out} gain={gain} loss={loss} net={net} total={self.total_money}"
            )

    @staticmethod
    def _bucket_metrics(bucket: dict[str, Any]) -> dict[str, Any]:
        n = int(bucket.get("n", 0))
        responses = int(bucket.get("responses", 0))
        timeouts = int(bucket.get("timeouts", 0))
        adv = int(bucket.get("adv", 0))

        rt_n = int(bucket.get("rt_n", 0))
        rt_sum = float(bucket.get("rt_sum", 0.0))

        timeout_rate = (timeouts / n) if n > 0 else 0.0
        advantageous_rate = (adv / responses) if responses > 0 else 0.0
        mean_rt_ms = (rt_sum / rt_n * 1000.0) if rt_n > 0 else 0.0

        deck_counts = {
            DECK_A: int(bucket.get(DECK_A, 0)),
            DECK_B: int(bucket.get(DECK_B, 0)),
            DECK_C: int(bucket.get(DECK_C, 0)),
            DECK_D: int(bucket.get(DECK_D, 0)),
        }

        return {
            "n": n,
            "responses": responses,
            "timeouts": timeouts,
            "timeout_rate": timeout_rate,
            "advantageous_rate": advantageous_rate,
            "mean_rt_ms": mean_rt_ms,
            "net_sum": int(bucket.get("net_sum", 0)),
            "gain_sum": int(bucket.get("gain_sum", 0)),
            "loss_sum": int(bucket.get("loss_sum", 0)),
            "deck_counts": deck_counts,
        }

    def total_metrics(self) -> dict[str, Any]:
        metrics = self._bucket_metrics(self.total_bucket)
        metrics["total_money"] = int(self.total_money)
        return metrics

    def block_metrics(self) -> dict[str, Any]:
        metrics = self._bucket_metrics(self.block_bucket)
        metrics["total_money"] = int(self.total_money)
        return metrics
