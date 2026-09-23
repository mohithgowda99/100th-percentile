# Research & Reuse Map

Reviewed: 24 Sep 2026

## What already exists

### Official GMAT
Use for ground truth, final calibration, section score trends and detailed performance insights. Official practice material should remain the highest-priority item source.

### GMAT Club
Already provides:
- large question bank and discussions;
- timer;
- error log;
- performance analytics;
- personalized recommendations;
- topic/difficulty tags;
- an active GMAT Question Patterns project.

The current Focus syllabus analysis is based on hundreds of official-style/official-prep questions and exposes useful top-level topic distributions. Their 2025-26 OG error-log spreadsheet is also useful as an external companion.

**Decision:** do not rebuild the question bank/timer/error-log shell. Use GMAT Club and official material as external practice surfaces while 100th Percentile adds structural labels, causal error diagnosis and learner-state decisions.

### GMAT Ninja
High-signal free instructional resource, especially for fundamentals, translation, elimination and avoiding formula-hoarding. Use as an intervention resource when a mastery node is weak rather than as a linear course to binge.

### catsim
Repository: https://github.com/douglasrizzo/catsim
BSD-3-Clause.
Reusable CAT simulation components: item selection, ability estimation, stopping rules and IRT item banks.

**Decision:** reuse for experiments only after we have meaningful item-response data. Do not pretend it reproduces GMAC's proprietary algorithm.

### py-irt
Repository: https://github.com/nd-ball/py-irt
Bayesian IRT estimation.

**Decision:** candidate for estimating item parameters from sufficient response data. Not useful for the first few weeks of a single learner.

### pyBKT
Repository: https://github.com/CAHLR/pyBKT
Models probability of skill mastery from sequential attempts, including guess/slip/learn parameters.

**Decision:** best first serious mastery model because it is interpretable and matches the skill-graph problem. Requires enough labelled sequential data.

### pyKT
Repository: https://github.com/pykt-team/pykt-toolkit
Benchmark library for many deep knowledge-tracing models.

**Decision:** research/evaluation tool later. Deep KT is unjustified for the initial n=1 phase and can overfit small data.

### FSRS
Organization: https://github.com/open-spaced-repetition
Evidence-backed open-source spaced repetition scheduler with implementations in many languages.

**Decision:** reuse for memory scheduling. Do not invent our own forgetting curve.

### Jev / TypeSafe AI
Best fit: bounded typed classification with inspectable uncertainty.

Use for:
- archetype;
- trap;
- error cause;
- prerequisite check;
- review routing.

Do not use as:
- math solver;
- tutor;
- proof engine.

Every Jev task must be benchmarked against human labels and a structured-output LLM baseline.

## High-signal community observations

Repeated themes in high-score debriefs:
- official material matters more than endless third-party volume;
- timing failures can erase strong knowledge;
- error review must identify the reason for the miss;
- verbal improves when answer elimination becomes explicit;
- official-mock scores can materially exceed or undershoot test-day scores, so robustness matters;
- pattern/archetype familiarity is repeatedly reported as useful, but blind keyword matching is dangerous.

Treat anecdotes as hypotheses, not ground truth.

## Our missing layer

No researched resource combines all four in a tight loop:

1. question structural decomposition;
2. causal learner-error diagnosis;
3. mastery/error graph;
4. next-best intervention chosen to maximize score improvement.

That is the product hypothesis.
