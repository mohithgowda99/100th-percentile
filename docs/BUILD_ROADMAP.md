# Build Roadmap — Score First

## North star

Primary: maximize Mohith's probability of 99th-percentile+ performance on 20 Nov 2026.

The app is only successful if official-mock / official-exam performance improves.

## v0.2 — usable now

- FastAPI web app
- responsive dashboard
- Quant foundation trainer
- mixed/interleaved trainer
- Skeleton Vision recognition mode
- timer + confidence capture
- skeleton / trap / explanation feedback
- local attempt database
- Atlas view
- mock logger
- transparent next-target recommendation
- CI tests

## v0.3 — immediately after Official Practice Exam 1

### 1. Diagnostic importer
Capture:
- Total / Q / V / DI
- per-question correctness
- time per question
- content / question type / skill tags
- review/edit behavior
- notes about freezes / guesses

Output:
- section bottlenecks
- timing bottlenecks
- primitive blockers
- highest-value 7-day prescription

### 2. Error Fingerprint UI
After a miss:
- self-report what happened
- combine self-report + question structure + timing + confidence
- keep multi-label uncertainty
- surface recurring causes

### 3. Quant dependency graph
Build the minimum prerequisite ladder:
- arithmetic
- fractions
- ratios
- percentages
- variables
- linear equations
- inequalities
- translation
- rates
- averages
- sets
- number properties
- counting/probability as needed

The graph should unlock skills just-in-time, not force a school-textbook sequence.

### 4. Pacing Guard
Official section structure:
- Quant: 21 questions / 45 minutes
- Verbal: 23 / 45
- DI: 20 / 45

Train:
- rolling time budget
- deliberate bail thresholds
- bookmark/review strategy
- intelligent guessing
- no unanswered questions

### 5. Contrast generator
Generate controlled pairs:
- same skeleton / different surface
- similar surface / different skeleton
- one-variable difficulty mutations
- explicit trap mutations

Synthetic questions are training weights, not score calibration.

## v0.4 — adaptive engine

- Jev archetype/trap/error classifier
- structured-LLM baseline
- human gold set
- classifier calibration / confidence routing
- FSRS review scheduling
- initial BKT mastery model once enough observations exist
- next-best-action policy driven by measured outcomes

## v0.5 — full GMAT

Expand ontology and trainer to:
- Critical Reasoning
- Reading Comprehension
- Data Sufficiency
- Table Analysis
- Graphics Interpretation
- Multi-Source Reasoning
- Two-Part Analysis

## v0.6 — 99th-percentile reliability

Train robustness, not just knowledge:
- hard mixed sets
- pacing under fatigue
- section-order experiments
- confidence calibration
- three-answer review/edit strategy
- exam-day simulation
- variance tracking across fresh official mocks

## Product validation

Do not infer product-market fit from "the app feels good."

Track:
- time to mastery
- error recurrence reduction
- recognition speed
- timed accuracy
- held-out transfer
- fresh official mock trajectory

If the system produces a large, reproducible score gain, then productize aggressively.
