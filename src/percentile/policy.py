from __future__ import annotations

from .models import LearnerSignal, Recommendation


DEFAULT_WEIGHTS = {
    "mastery_gap": 0.27,
    "timed_gap": 0.12,
    "error_recurrence": 0.18,
    "memory_due": 0.12,
    "exam_relevance": 0.18,
    "prerequisite_blocking": 0.10,
    "overexposure": 0.12,
}


def rank_next_actions(
    signals: list[LearnerSignal],
    weights: dict[str, float] | None = None,
) -> list[Recommendation]:
    """Rank study targets by expected training value.

    This is intentionally a transparent bootstrap policy, not a claim to be an
    optimal tutor. As attempt data accumulates, weights should be evaluated
    against held-out performance and official mock outcomes.
    """

    w = DEFAULT_WEIGHTS | (weights or {})
    recommendations: list[Recommendation] = []

    for signal in signals:
        mastery_gap = 1.0 - signal.mastery_probability
        timed_gap = 1.0 - signal.timed_accuracy

        score = (
            w["mastery_gap"] * mastery_gap
            + w["timed_gap"] * timed_gap
            + w["error_recurrence"] * signal.error_recurrence
            + w["memory_due"] * signal.memory_due
            + w["exam_relevance"] * signal.exam_relevance
            + w["prerequisite_blocking"] * signal.prerequisite_blocking
            - w["overexposure"] * signal.overexposure
        )

        reasons: list[str] = []
        if mastery_gap >= 0.35:
            reasons.append("LOW_MASTERY")
        if signal.error_recurrence >= 0.35:
            reasons.append("RECURRING_ERROR")
        if signal.memory_due >= 0.6:
            reasons.append("MEMORY_DUE")
        if signal.exam_relevance >= 0.7:
            reasons.append("HIGH_EXAM_RELEVANCE")
        if signal.prerequisite_blocking >= 0.4:
            reasons.append("PREREQUISITE_BLOCKER")
        if timed_gap >= 0.35:
            reasons.append("TIMING_GAP")

        recommendations.append(
            Recommendation(
                target_id=signal.id,
                score=score,
                reason_codes=tuple(reasons),
            )
        )

    return sorted(recommendations, key=lambda item: item.score, reverse=True)
