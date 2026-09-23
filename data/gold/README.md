# Gold-set format

The classifier benchmark must start from human-labelled examples.

Do not add copyrighted paid question text. Store a reference plus derived labels.

## Gold JSONL

Each line:

```json
{"id":"og26-q-001","task":"primary_archetype","true_label":"Q_ALG_LINEAR","question_ref":"OG 2026-2027 / Quant / #1","reviewer":"human","notes":""}
```

Recommended initial set:
- 50 Quant;
- 30 Critical Reasoning;
- 20 Reading Comprehension;
- 50 Data Insights;
- stratified across difficulty and known archetypes.

Double-label ambiguous examples and adjudicate disagreements.

## Prediction JSONL

```json
{"id":"og26-q-001","task":"primary_archetype","predicted_label":"Q_ALG_LINEAR","classifier":"jev","classifier_version":"...","review_required":false,"probabilities":{"Q_ALG_LINEAR":0.84,"Q_PERCENT":0.09,"OTHER":0.07}}
```

Run the same IDs through Jev and a structured-output LLM. Compare accuracy, macro F1, Brier score and high-confidence coverage.
