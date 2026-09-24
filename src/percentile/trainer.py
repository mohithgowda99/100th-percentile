from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import random

from .models import ErrorCause, LearnerSignal
from .policy import rank_next_actions
from .questions import Question, SEED_QUESTIONS


class SessionMode(StrEnum):
    FOUNDATION = "foundation"
    MIXED = "mixed"
    RECOGNITION = "recognition"


@dataclass(frozen=True)
class ScoredAnswer:
    correct: bool
    correct_index: int
    explanation: str
    skeleton: str
    trap: str
    likely_error: ErrorCause | None


def build_session(mode: SessionMode = SessionMode.FOUNDATION, limit: int = 8, seed: int | None = None) -> list[Question]:
    rng = random.Random(seed)
    pool = list(SEED_QUESTIONS)
    if mode == SessionMode.FOUNDATION:
        pool.sort(key=lambda q: (q.difficulty, q.id))
        return pool[: min(limit, len(pool))]
    rng.shuffle(pool)
    return pool[: min(limit, len(pool))]


def score_answer(question: Question, selected_index: int) -> ScoredAnswer:
    correct = selected_index == question.correct_index
    return ScoredAnswer(
        correct=correct,
        correct_index=question.correct_index,
        explanation=question.explanation,
        skeleton=question.skeleton,
        trap=question.trap,
        likely_error=None if correct else question.likely_error_if_wrong,
    )


def signals_from_skill_stats(stats: dict[str, dict[str, float]]) -> list[LearnerSignal]:
    signals: list[LearnerSignal] = []
    for skill_id, row in stats.items():
        attempts = max(int(row.get("attempts", 0)), 1)
        accuracy = row.get("correct", 0.0) / attempts
        slow_rate = row.get("slow", 0.0) / attempts
        recurrence = row.get("errors", 0.0) / attempts
        signals.append(
            LearnerSignal(
                id=skill_id,
                mastery_probability=max(0.05, min(0.95, accuracy)),
                timed_accuracy=max(0.0, min(1.0, accuracy * (1.0 - 0.35 * slow_rate))),
                error_recurrence=max(0.0, min(1.0, recurrence)),
                memory_due=0.35,
                exam_relevance=0.8,
                prerequisite_blocking=0.7 if accuracy < 0.6 else 0.15,
                overexposure=min(1.0, attempts / 30.0),
            )
        )
    return signals


def recommend_from_skill_stats(stats: dict[str, dict[str, float]]):
    signals = signals_from_skill_stats(stats)
    return rank_next_actions(signals) if signals else []
