# 100th Percentile — Product & Training Spec v0.1

Status: **active**
Target exam: **20 Nov 2026**
Target: **99th percentile+; engineer toward 735+ rather than barely clearing the threshold**

## 1. Objective function

This repository exists to maximize exam score, not software sophistication.

Primary metric:
- Official GMAT practice / official exam score and section subscores.

Leading metrics:
- archetype recognition accuracy;
- primitive mastery;
- trap-resistance accuracy;
- time-to-correct solution;
- error recurrence rate;
- mixed-set accuracy under time pressure;
- calibration gap between confidence and actual correctness.

A feature that does not plausibly move one of these metrics is deferred.

## 2. Core hypothesis

GMAT questions vary heavily in surface form but recur in a bounded set of reasoning structures. Performance can improve faster if the learner is trained to:

1. recognize the underlying archetype;
2. map it to a small set of reasoning primitives;
3. execute a canonical solution strategy;
4. detect common traps;
5. diagnose the true cause of errors;
6. revisit skills at the right time;
7. practice mixed/disguised variants until recognition generalizes.

This is **not** keyword matching. Anti-pattern drills must deliberately use similar surface wording with different underlying structures.

## 3. Product wedge

Existing products already solve large pieces:
- GMAT Club: question bank, timer, error log, analytics, difficulty data, topic tagging, adaptive recommendations, and a growing Question Patterns project.
- Official GMAT: authentic items, six official practice exams, detailed performance insights.
- FSRS: evidence-based review scheduling.
- pyBKT / knowledge tracing: probabilistic skill mastery.
- catsim / IRT tooling: CAT simulation and ability estimation.

Therefore our wedge is not "another prep platform."

Our wedge is:

**Question -> structural decomposition -> learner failure diagnosis -> mastery update -> next-best intervention**

## 4. System model

### 4.1 Pattern Atlas

Every item may be described by metadata only:

- source reference / question ID;
- section;
- format;
- primary archetype;
- subtype;
- reasoning primitives;
- common traps;
- solution strategies;
- difficulty band;
- representation/disguise;
- prerequisite skills;
- related archetypes;
- provenance;
- human-validation status.

Official question text is not required in the repository.

### 4.2 Reasoning primitives

Initial cross-section primitives:

Quant:
- translate
- normalize
- isolate
- substitute
- factor
- compare
- bound
- estimate
- enumerate_cases
- backsolve
- test_values
- unit_convert
- proportional_reasoning
- weighted_average
- set_overlap

Verbal:
- identify_conclusion
- identify_evidence
- identify_assumption
- negate_assumption
- causal_alternative
- scope_check
- strength_check
- inference_only
- resolve_discrepancy
- eliminate_unsupported
- map_passage_structure

Data Insights:
- sufficiency_not_value
- filter
- sort
- denominator_check
- cross_source_reconcile
- relevance_filter
- constraint_intersection
- graph_read
- conditional_reasoning
- two_part_dependency

The ontology is expected to change. IDs must remain stable once attempts reference them.

### 4.3 Error Fingerprint

Errors are causal, not just topical.

Initial taxonomy:
- K1_CONCEPT_UNKNOWN
- K2_CONCEPT_NOT_RETRIEVABLE
- R1_ARCHETYPE_NOT_RECOGNIZED
- R2_FALSE_PATTERN_MATCH
- T1_TRANSLATION_FAILURE
- E1_EXECUTION_LOGIC
- A1_ARITHMETIC
- C1_CONSTRAINT_MISSED
- X1_TRAP_SELECTED
- P1_PACING
- P2_OVERINVESTED_TIME
- G1_LOW_INFORMATION_GUESS
- M1_MISREAD
- V1_VERBAL_SCOPE
- V2_VERBAL_STRENGTH
- D1_DATA_EXTRACTION
- D2_DENOMINATOR_BASE_RATE
- U1_UNCLASSIFIED

Error classification should preserve uncertainty and may be multi-label.

### 4.4 Learner state

Per skill/archetype track:
- mastery probability;
- recent accuracy;
- timed accuracy;
- median response time;
- confidence calibration;
- recurring error causes;
- last reviewed;
- memory due state;
- evidence count.

Do not fit complex models before enough observations exist.

### 4.5 Next-best-action policy

Candidate practice should be ranked by expected score value, not random topic rotation.

Inputs:
- mastery gap;
- exam relevance / prevalence;
- error recurrence;
- prerequisite blocking value;
- memory due-ness;
- target difficulty;
- timing weakness;
- novelty / disguise distance;
- recent overexposure penalty;
- official-material priority.

The policy should output both a selection and a machine-readable reason.

## 5. Jev role

Jev is a candidate **bounded classifier**, not the tutor and not the source of mathematical truth.

Good Jev tasks:
- archetype Choice;
- trap Choice;
- error-cause Choice;
- difficulty Score;
- prerequisite-present yes/no;
- "needs human review" routing using uncertainty.

Bad Jev tasks:
- long-form teaching;
- mathematical proof;
- generating explanations;
- unbounded taxonomy discovery.

### Benchmark requirement

Create a human-labelled gold set before trusting automation.

Benchmark:
- Jev;
- structured-output LLM;
- simple rules/baseline where appropriate.

Metrics:
- top-1 accuracy;
- macro F1;
- Brier score when probabilities exist;
- coverage at confidence threshold;
- error cost by label.

No classifier graduates based on vibes.

## 6. Reuse plan

### CAT / IRT
Use existing packages such as `catsim` and `py-irt` if/when we have enough item-response data. We are not attempting to clone GMAC's proprietary scoring algorithm.

### Knowledge tracing
Start with an interpretable mastery model. Evaluate `pyBKT` after collecting enough sequential attempts. Only benchmark deep KT (e.g. pyKT) when dataset size justifies it.

### Spaced repetition
Use FSRS rather than inventing review intervals.

### Official calibration
Synthetic/generated drills are for repetition and contrast. Official GMAT questions and official practice exams are the calibration layer.

## 7. Copyright / integrity boundary

Store:
- official item identifiers;
- book/test references;
- derived labels;
- learner attempt metadata;
- original synthetic questions;
- links to publicly accessible discussions.

Do not commit:
- copied paid question banks;
- scraped copyrighted official item text;
- leaked/recalled live exam content.

## 8. 57-day operating plan

Phase 0 — baseline:
- take Official Practice Exam 1 cold;
- import Total/Q/V/DI, question-level timing if available, and performance insights;
- establish weakest primitives and error modes.

Phase 1 — foundation repair:
- arithmetic;
- fractions/ratios/percentages;
- variables;
- linear equations;
- word-to-equation translation;
- only enough theory to unlock GMAT applications.

Phase 2 — archetype acquisition:
- official-question-heavy practice;
- Skeleton Vision drills;
- contrast pairs / anti-patterns;
- error fingerprinting.

Phase 3 — mixed timed execution:
- hard mixed sets;
- pacing;
- confidence calibration;
- deliberate guessing;
- trap resistance.

Phase 4 — CAT stabilization:
- official practice exams;
- deep post-mock autopsy;
- target the few failure modes causing most score loss.

Phase 5 — taper:
- no broad new content;
- maintain retrieval;
- eliminate recurring errors;
- protect sleep and test-day execution.

## 9. MVP interfaces

### Question metadata
The engine should accept an item reference plus structural labels without needing copyrighted text.

### Attempt
Minimum event:
- question_ref
- timestamp
- correct
- response_seconds
- confidence
- selected_answer (optional)
- section
- user_note (optional)
- self_reported_error (optional)

### Classification output
- label;
- probability/confidence;
- alternatives;
- classifier;
- classifier_version;
- review_required.

### Recommendation output
- next_skill/archetype;
- activity_type;
- target difficulty;
- reason codes;
- expected objective.

## 10. Evaluation

### Classifier eval
Human-labelled stratified set across Q/V/DI.

### Training-policy eval
Within-person:
- pre/post accuracy on held-out official-like structures;
- time reduction;
- recurrence reduction;
- official mock score trajectory.

Product validation should eventually compare users or alternate training policies, but the first n=1 experiment is Mohith.

## 11. Kill criteria

Pause or remove:
- any classifier that does not beat a trivial baseline;
- deep KT before sufficient data;
- CAT emulation that does not change study decisions;
- social/community features;
- polished frontend;
- large synthetic question generation before validation;
- anything that delays official-question practice.

## 12. Immediate backlog

P0
- official cold diagnostic;
- initial ontology;
- attempt schema;
- gold-label format;
- classifier eval harness;
- error fingerprint;
- daily recommendation output.

P1
- Jev adapter;
- structured LLM adapter;
- FSRS adapter;
- pyBKT experiment;
- question-pair contrast trainer;
- mock autopsy importer.

P2
- CAT simulation;
- richer knowledge tracing;
- consumer UI;
- multi-user product analytics.
