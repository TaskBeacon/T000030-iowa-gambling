from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context

from .utils import ADVANTAGEOUS_DECKS, DECK_A, DECK_B, DECK_C, DECK_D


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _as_duration(controller, value: Any, default_value: float) -> float:
    if hasattr(controller, "sample_duration"):
        return float(controller.sample_duration(value, default_value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return float(default_value)
    return float(default_value)


def _trial_id(controller) -> int:
    if hasattr(controller, "next_trial_id"):
        return int(controller.next_trial_id())
    return 1


def _task_dict(settings, attr_name: str) -> dict[str, Any]:
    value = getattr(settings, attr_name, {})
    return value if isinstance(value, dict) else {}


def _deck_key_map(settings) -> dict[str, str]:
    return {
        DECK_A: str(getattr(settings, "deck_a_key", "d")).strip().lower(),
        DECK_B: str(getattr(settings, "deck_b_key", "f")).strip().lower(),
        DECK_C: str(getattr(settings, "deck_c_key", "j")).strip().lower(),
        DECK_D: str(getattr(settings, "deck_d_key", "k")).strip().lower(),
    }


def _deck_label_map(settings) -> dict[str, str]:
    configured = _task_dict(settings, "deck_labels")
    return {
        DECK_A: str(configured.get(DECK_A, "A")),
        DECK_B: str(configured.get(DECK_B, "B")),
        DECK_C: str(configured.get(DECK_C, "C")),
        DECK_D: str(configured.get(DECK_D, "D")),
    }


def _deck_from_key(response_key: str, deck_keys: dict[str, str]) -> str | None:
    key = str(response_key or "").strip().lower()
    for deck, deck_key in deck_keys.items():
        if key == deck_key:
            return deck
    return None


def _choice_trigger(deck_id: str) -> str:
    mapping = {
        DECK_A: "choice_deck_a",
        DECK_B: "choice_deck_b",
        DECK_C: "choice_deck_c",
        DECK_D: "choice_deck_d",
    }
    return mapping.get(deck_id, "")


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one Iowa Gambling Task trial (fixation -> decision -> feedback -> iti)."""
    trial_id = _trial_id(controller)
    condition_name = str(getattr(controller, "parse_condition", lambda c: c)(condition)).strip().lower()
    block_label = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0

    deck_keys = _deck_key_map(settings)
    deck_labels = _deck_label_map(settings)
    response_keys = [deck_keys[DECK_A], deck_keys[DECK_B], deck_keys[DECK_C], deck_keys[DECK_D]]

    fixation_duration = _as_duration(controller, settings.fixation_duration, 0.4)
    decision_deadline = float(getattr(settings, "decision_deadline", 3.5))
    feedback_duration = float(getattr(settings, "feedback_duration", 1.0))
    iti_duration = _as_duration(controller, settings.iti_duration, 0.45)

    balance_before = int(getattr(controller, "total_money", 0))
    trial_data = {
        "condition": condition_name,
        "trial_id": trial_id,
        "block_id": block_label,
        "block_idx": block_index,
        "balance_before": balance_before,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=_deadline_s(fixation_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=condition_name,
        task_factors={"stage": "fixation", "block_idx": block_index},
        stim_id="fixation",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    decision = make_unit(unit_label="decision")
    decision.add_stim(stim_bank.get("decision_title"))
    decision.add_stim(stim_bank.get_and_format("balance_text", current_total=balance_before))
    decision.add_stim(stim_bank.get("deck_a_rect"))
    decision.add_stim(stim_bank.get("deck_b_rect"))
    decision.add_stim(stim_bank.get("deck_c_rect"))
    decision.add_stim(stim_bank.get("deck_d_rect"))
    decision.add_stim(stim_bank.get_and_format("deck_a_label", deck_a_key=deck_keys[DECK_A].upper()))
    decision.add_stim(stim_bank.get_and_format("deck_b_label", deck_b_key=deck_keys[DECK_B].upper()))
    decision.add_stim(stim_bank.get_and_format("deck_c_label", deck_c_key=deck_keys[DECK_C].upper()))
    decision.add_stim(stim_bank.get_and_format("deck_d_label", deck_d_key=deck_keys[DECK_D].upper()))
    decision.add_stim(stim_bank.get("key_hint"))
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="decision",
        deadline_s=_deadline_s(decision_deadline),
        valid_keys=response_keys,
        block_id=block_label,
        condition_id=condition_name,
        task_factors={
            "stage": "decision",
            "deck_a_key": deck_keys[DECK_A],
            "deck_b_key": deck_keys[DECK_B],
            "deck_c_key": deck_keys[DECK_C],
            "deck_d_key": deck_keys[DECK_D],
            "current_total": balance_before,
            "block_idx": block_index,
        },
        stim_id="decision_title+balance_text+deck_rects+deck_labels+key_hint",
    )
    decision.capture_response(
        keys=response_keys,
        duration=decision_deadline,
        onset_trigger=settings.triggers.get("decision_onset"),
        response_trigger=None,
        timeout_trigger=settings.triggers.get("choice_timeout"),
    )
    decision.to_dict(trial_data)

    response_key = str(decision.get_state("response", "")).strip().lower()
    timed_out = response_key not in response_keys
    chosen_deck = _deck_from_key(response_key, deck_keys) if not timed_out else None

    rt = decision.get_state("rt", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None

    gain = 0
    loss = 0
    net = 0
    draw_index = 0
    balance_after = balance_before
    deck_label = ""

    if chosen_deck:
        trigger_runtime.send(settings.triggers.get(_choice_trigger(chosen_deck)))
        draw = controller.draw_from_deck(chosen_deck)
        gain = int(draw["gain"])
        loss = int(draw["loss"])
        net = int(draw["net"])
        draw_index = int(draw["draw_index"])
        balance_after = int(draw["total_money"])
        deck_label = deck_labels.get(chosen_deck, chosen_deck.upper())
    else:
        balance_after = int(getattr(controller, "total_money", balance_before))

    if timed_out:
        feedback_stim_id = "feedback_timeout"
        feedback_stim = stim_bank.get_and_format("feedback_timeout", balance_after=balance_after)
    else:
        feedback_stim_id = "feedback_outcome"
        feedback_stim = stim_bank.get_and_format(
            "feedback_outcome",
            deck_label=deck_label,
            gain=gain,
            loss=loss,
            net=net,
            balance_after=balance_after,
        )

    feedback = make_unit(unit_label="feedback").add_stim(feedback_stim)
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=_deadline_s(feedback_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=condition_name,
        task_factors={
            "stage": "feedback",
            "chosen_deck": chosen_deck or "",
            "timed_out": timed_out,
            "gain": gain,
            "loss": loss,
            "net": net,
            "balance_after": balance_after,
            "block_idx": block_index,
        },
        stim_id=feedback_stim_id,
    )
    feedback.show(
        duration=feedback_duration,
        onset_trigger=settings.triggers.get("feedback_onset"),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=_deadline_s(iti_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=condition_name,
        task_factors={"stage": "iti", "block_idx": block_index},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    advantageous_choice = bool(chosen_deck in ADVANTAGEOUS_DECKS) if chosen_deck else False
    trial_data.update(
        {
            "chosen_deck": chosen_deck or "",
            "response_key": response_key if not timed_out else "",
            "timed_out": bool(timed_out),
            "rt_s": rt_s,
            "decision_rt_s": rt_s,
            "decision_timed_out": bool(timed_out),
            "gain": int(gain),
            "loss": int(loss),
            "net_outcome": int(net),
            "draw_index": int(draw_index),
            "balance_after": int(balance_after),
            "advantageous_choice": advantageous_choice,
        }
    )

    controller.record_trial(
        deck=chosen_deck,
        rt_s=rt_s,
        timed_out=bool(timed_out),
        gain=int(gain),
        loss=int(loss),
        net=int(net),
    )
    return trial_data
