from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from math import fsum
from typing import Iterable, Mapping, Sequence

from .models import Classification


@dataclass(frozen=True)
class GoldExample:
    id: str
    true_label: str


@dataclass(frozen=True)
class EvalResult:
    count: int
    accuracy: float
    macro_f1: float
    brier: float
    coverage: float
    covered_accuracy: float | None


def _f1(tp: int, fp: int, fn: int) -> float:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0.0
    )


def evaluate(
    gold: Mapping[str, str],
    predictions: Mapping[str, Classification],
    confidence_threshold: float = 0.0,
) -> EvalResult:
    common = sorted(set(gold) & set(predictions))
    if not common:
        raise ValueError("No overlapping gold and prediction IDs")

    labels = sorted({gold[i] for i in common} | {predictions[i].predicted_label for i in common})

    correct = 0
    brier_terms: list[float] = []
    covered = 0
    covered_correct = 0

    for item_id in common:
        truth = gold[item_id]
        prediction = predictions[item_id]
        if prediction.predicted_label == truth:
            correct += 1

        # Multiclass Brier score: mean squared probability error across labels.
        brier_terms.append(
            fsum(
                (prediction.probability_for(label) - (1.0 if label == truth else 0.0)) ** 2
                for label in labels
            )
            / len(labels)
        )

        top_probability = max(
            (p.probability for p in prediction.probabilities),
            default=1.0 if not prediction.review_required else 0.0,
        )
        if top_probability >= confidence_threshold and not prediction.review_required:
            covered += 1
            if prediction.predicted_label == truth:
                covered_correct += 1

    f1_scores: list[float] = []
    for label in labels:
        tp = fp = fn = 0
        for item_id in common:
            truth = gold[item_id]
            pred = predictions[item_id].predicted_label
            tp += int(truth == label and pred == label)
            fp += int(truth != label and pred == label)
            fn += int(truth == label and pred != label)
        f1_scores.append(_f1(tp, fp, fn))

    count = len(common)
    return EvalResult(
        count=count,
        accuracy=correct / count,
        macro_f1=fsum(f1_scores) / len(f1_scores),
        brier=fsum(brier_terms) / count,
        coverage=covered / count,
        covered_accuracy=(covered_correct / covered) if covered else None,
    )
