from percentile.evaluation import evaluate
from percentile.models import Classification, LabelProbability, LearnerSignal
from percentile.policy import rank_next_actions


def prediction(label: str, p: float, other: str = "other") -> Classification:
    return Classification(
        task="archetype",
        predicted_label=label,
        probabilities=(
            LabelProbability(label, p),
            LabelProbability(other, 1 - p),
        ),
        classifier="test",
        classifier_version="0",
    )


def test_evaluate_perfect_predictions():
    gold = {"a": "rate", "b": "algebra"}
    predictions = {
        "a": prediction("rate", 0.9),
        "b": prediction("algebra", 0.8),
    }
    result = evaluate(gold, predictions)
    assert result.count == 2
    assert result.accuracy == 1.0
    assert result.macro_f1 == 1.0
    assert result.brier >= 0.0


def test_confidence_threshold_changes_coverage():
    gold = {"a": "rate", "b": "algebra"}
    predictions = {
        "a": prediction("rate", 0.95),
        "b": prediction("algebra", 0.55),
    }
    result = evaluate(gold, predictions, confidence_threshold=0.8)
    assert result.coverage == 0.5
    assert result.covered_accuracy == 1.0


def test_policy_prioritizes_blocking_weakness():
    weak = LearnerSignal(
        id="linear-equations",
        mastery_probability=0.25,
        timed_accuracy=0.4,
        error_recurrence=0.7,
        memory_due=0.8,
        exam_relevance=0.9,
        prerequisite_blocking=0.9,
    )
    strong = LearnerSignal(
        id="percentages",
        mastery_probability=0.9,
        timed_accuracy=0.9,
        error_recurrence=0.05,
        memory_due=0.1,
        exam_relevance=0.9,
    )
    ranked = rank_next_actions([strong, weak])
    assert ranked[0].target_id == "linear-equations"
    assert "PREREQUISITE_BLOCKER" in ranked[0].reason_codes
