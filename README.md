# 100th Percentile

A score-optimization system for the GMAT.

Primary objective: maximize Mohith's probability of scoring **99th percentile+ on 20 Nov 2026**.

Secondary objective: validate whether the system creates enough measurable learning advantage to become a product.

## Product thesis

The GMAT is a bounded reasoning system with recurring archetypes, traps, and skill dependencies. The product should compress the test into a learnable pattern graph, diagnose why a learner misses questions, and choose the highest-value next action.

## Non-goals

- Rebuild GMAT Club's question bank, timer, or generic error log.
- Reimplement IRT/CAT, spaced repetition, or knowledge-tracing algorithms that already exist.
- Store or redistribute copyrighted official GMAT question text.
- Build polished UI before the training engine demonstrates score lift.
- Treat an LLM's confidence as ground truth.

## Build vs reuse

Reuse:
- Official GMAT material as ground truth and official practice exams for calibration.
- GMAT Club pattern/topic metadata and community discussion as research inputs.
- `catsim` / IRT tooling for CAT experiments.
- `pyBKT` initially for interpretable skill mastery; benchmark deeper KT only after enough data exists.
- FSRS for memory/review scheduling.
- Jev and structured LLM outputs as competing classifiers, evaluated on a human-labelled gold set.

Build:
- GMAT Pattern Atlas ontology.
- Error Fingerprint taxonomy.
- Skeleton Vision recognition drills.
- Learner-specific mastery/error graph.
- Next-best-question policy combining mastery gap, recurrence, timing, error history, novelty and memory due-ness.
- Classifier evaluation harness.

## First milestone

**Atlas v0.1** is successful when:
1. A manually labelled gold set exists.
2. Questions can be tagged into stable archetypes/primitives/traps.
3. Jev and an LLM classifier can be compared objectively.
4. Attempts create an Error Fingerprint.
5. The engine produces a reasoned next-best training action.
6. Mohith's official-mock performance improves.

See [SPEC.md](SPEC.md).


## Run the web app

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
percentile-web
```

Open `http://127.0.0.1:8000`.

Current usable slice:
- responsive dashboard;
- Quant foundation and mixed sessions;
- **Skeleton Vision** archetype-recognition mode;
- timer + confidence capture;
- skeleton/trap/solution feedback;
- local learner-state database;
- Atlas view;
- official-mock logging;
- transparent next-target recommendation.

The seed questions are original synthetic drills. Official GMAT material remains the calibration layer and is referenced by metadata rather than copied into the repository.
