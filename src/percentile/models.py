from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Mapping, Sequence


class Section(StrEnum):
    QUANT = "quant"
    VERBAL = "verbal"
    DATA_INSIGHTS = "data_insights"


class ErrorCause(StrEnum):
    CONCEPT_UNKNOWN = "K1_CONCEPT_UNKNOWN"
    CONCEPT_NOT_RETRIEVABLE = "K2_CONCEPT_NOT_RETRIEVABLE"
    ARCHETYPE_NOT_RECOGNIZED = "R1_ARCHETYPE_NOT_RECOGNIZED"
    FALSE_PATTERN_MATCH = "R2_FALSE_PATTERN_MATCH"
    TRANSLATION_FAILURE = "T1_TRANSLATION_FAILURE"
    EXECUTION_LOGIC = "E1_EXECUTION_LOGIC"
    ARITHMETIC = "A1_ARITHMETIC"
    CONSTRAINT_MISSED = "C1_CONSTRAINT_MISSED"
    TRAP_SELECTED = "X1_TRAP_SELECTED"
    PACING = "P1_PACING"
    OVERINVESTED_TIME = "P2_OVERINVESTED_TIME"
    LOW_INFORMATION_GUESS = "G1_LOW_INFORMATION_GUESS"
    MISREAD = "M1_MISREAD"
    VERBAL_SCOPE = "V1_VERBAL_SCOPE"
    VERBAL_STRENGTH = "V2_VERBAL_STRENGTH"
    DATA_EXTRACTION = "D1_DATA_EXTRACTION"
    DENOMINATOR_BASE_RATE = "D2_DENOMINATOR_BASE_RATE"
    UNCLASSIFIED = "U1_UNCLASSIFIED"


@dataclass(frozen=True)
class Attempt:
    question_ref: str
    section: Section
    correct: bool
    response_seconds: float
    confidence: float | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    archetype_ids: tuple[str, ...] = ()
    skill_ids: tuple[str, ...] = ()
    self_reported_error: ErrorCause | None = None
    user_note: str | None = None

    def __post_init__(self) -> None:
        if self.response_seconds < 0:
            raise ValueError("response_seconds must be non-negative")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class LabelProbability:
    label: str
    probability: float

    def __post_init__(self) -> None:
        if not 0 <= self.probability <= 1:
            raise ValueError("probability must be between 0 and 1")


@dataclass(frozen=True)
class Classification:
    task: str
    predicted_label: str
    probabilities: tuple[LabelProbability, ...]
    classifier: str
    classifier_version: str
    review_required: bool = False

    def probability_for(self, label: str) -> float:
        for item in self.probabilities:
            if item.label == label:
                return item.probability
        return 0.0


@dataclass(frozen=True)
class LearnerSignal:
    id: str
    mastery_probability: float
    timed_accuracy: float
    error_recurrence: float
    memory_due: float
    exam_relevance: float
    prerequisite_blocking: float = 0.0
    overexposure: float = 0.0

    def __post_init__(self) -> None:
        for name, value in (
            ("mastery_probability", self.mastery_probability),
            ("timed_accuracy", self.timed_accuracy),
            ("error_recurrence", self.error_recurrence),
            ("memory_due", self.memory_due),
            ("exam_relevance", self.exam_relevance),
            ("prerequisite_blocking", self.prerequisite_blocking),
            ("overexposure", self.overexposure),
        ):
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class Recommendation:
    target_id: str
    score: float
    reason_codes: tuple[str, ...]
