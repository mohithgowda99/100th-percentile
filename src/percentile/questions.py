from __future__ import annotations

from dataclasses import dataclass

from .models import Section, ErrorCause


@dataclass(frozen=True)
class Question:
    id: str
    section: Section
    archetype_id: str
    archetype_name: str
    skill_ids: tuple[str, ...]
    prompt: str
    options: tuple[str, ...]
    correct_index: int
    explanation: str
    skeleton: str
    trap: str
    difficulty: int
    likely_error_if_wrong: ErrorCause


SEED_QUESTIONS: tuple[Question, ...] = (
    Question(
        id="Q-LIN-001",
        section=Section.QUANT,
        archetype_id="Q_ALG_LINEAR",
        archetype_name="Linear equations",
        skill_ids=("isolate_variable",),
        prompt="If 3x + 7 = 22, what is x?",
        options=("3", "4", "5", "6", "7"),
        correct_index=2,
        explanation="Subtract 7 from both sides: 3x = 15. Divide by 3: x = 5.",
        skeleton="ax + b = c → subtract b → divide by a.",
        trap="Changing sides without preserving equality, or dividing before removing the constant.",
        difficulty=1,
        likely_error_if_wrong=ErrorCause.EXECUTION_LOGIC,
    ),
    Question(
        id="Q-LIN-002",
        section=Section.QUANT,
        archetype_id="Q_ALG_LINEAR",
        archetype_name="Linear equations",
        skill_ids=("translate_to_equation", "isolate_variable"),
        prompt="A gym charges a fixed joining fee of $18 plus $7 per visit. Maya paid $67 in total. How many visits did she make?",
        options=("5", "6", "7", "8", "9"),
        correct_index=2,
        explanation="Translate first: 18 + 7v = 67. Then 7v = 49, so v = 7.",
        skeleton="fixed amount + rate × quantity = total.",
        trap="Treating the fixed fee as part of the per-visit rate.",
        difficulty=2,
        likely_error_if_wrong=ErrorCause.TRANSLATION_FAILURE,
    ),
    Question(
        id="Q-LIN-003",
        section=Section.QUANT,
        archetype_id="Q_ALG_LINEAR",
        archetype_name="Linear equations",
        skill_ids=("translate_to_equation", "substitute"),
        prompt="Twice a number is 9 more than the number. What is the number?",
        options=("7", "8", "9", "10", "11"),
        correct_index=2,
        explanation="Let the number be x. 'Twice a number is 9 more than the number' means 2x = x + 9. Therefore x = 9.",
        skeleton="verbal relationship → equation between two expressions.",
        trap="Translating '9 more than' as subtraction.",
        difficulty=2,
        likely_error_if_wrong=ErrorCause.TRANSLATION_FAILURE,
    ),
    Question(
        id="Q-PCT-001",
        section=Section.QUANT,
        archetype_id="Q_PERCENT",
        archetype_name="Percent change",
        skill_ids=("percent_multiplier",),
        prompt="A price is increased by 20% and then decreased by 20%. Relative to the original price, the final price is:",
        options=("4% lower", "unchanged", "4% higher", "8% lower", "8% higher"),
        correct_index=0,
        explanation="Normalize the original to 100. After +20% it is 120; after -20% it is 96. Final = 4% lower.",
        skeleton="successive percentage changes multiply: original × 1.20 × 0.80.",
        trap="Adding +20% and -20% and assuming they cancel.",
        difficulty=2,
        likely_error_if_wrong=ErrorCause.TRAP_SELECTED,
    ),
    Question(
        id="Q-PCT-002",
        section=Section.QUANT,
        archetype_id="Q_PERCENT",
        archetype_name="Reverse percentage",
        skill_ids=("reverse_percent",),
        prompt="After a 20% discount, a jacket costs $80. What was the original price?",
        options=("$96", "$100", "$104", "$120", "$125"),
        correct_index=1,
        explanation="After a 20% discount, 80% of the original remains. 0.8 × original = 80, so original = 100.",
        skeleton="known final = remaining multiplier × original → divide by multiplier.",
        trap="Adding 20% of the discounted price instead of reversing the multiplier.",
        difficulty=2,
        likely_error_if_wrong=ErrorCause.FALSE_PATTERN_MATCH,
    ),
    Question(
        id="Q-RATIO-001",
        section=Section.QUANT,
        archetype_id="Q_PERCENT",
        archetype_name="Ratios and proportions",
        skill_ids=("ratio_parts",),
        prompt="The ratio of red to blue marbles is 2:3. If there are 35 marbles in total, how many are red?",
        options=("12", "14", "15", "20", "21"),
        correct_index=1,
        explanation="There are 5 ratio parts in total. Each part is 35/5 = 7. Red = 2 × 7 = 14.",
        skeleton="part : part → total parts → value per part.",
        trap="Using 2/3 of the total instead of 2/(2+3).",
        difficulty=1,
        likely_error_if_wrong=ErrorCause.DENOMINATOR_BASE_RATE,
    ),
    Question(
        id="Q-RATE-001",
        section=Section.QUANT,
        archetype_id="Q_RATE_WORK",
        archetype_name="Work and rate",
        skill_ids=("work_rate", "fraction_addition"),
        prompt="Worker A completes a job in 6 hours and Worker B in 3 hours. Working together at constant rates, how long do they take?",
        options=("1 hour", "2 hours", "2.5 hours", "3 hours", "4 hours"),
        correct_index=1,
        explanation="A's rate is 1/6 job/hour and B's is 1/3. Together: 1/6 + 1/3 = 1/2 job/hour, so one job takes 2 hours.",
        skeleton="individual time → reciprocal rates → add rates → reciprocal back to time.",
        trap="Averaging the completion times directly.",
        difficulty=2,
        likely_error_if_wrong=ErrorCause.ARCHETYPE_NOT_RECOGNIZED,
    ),
    Question(
        id="Q-RATE-002",
        section=Section.QUANT,
        archetype_id="Q_RATE_DISTANCE",
        archetype_name="Distance and speed",
        skill_ids=("average_speed_equal_distance",),
        prompt="A car travels the same distance at 60 km/h and then at 40 km/h. What is its average speed for the entire trip?",
        options=("45", "48", "50", "52", "54"),
        correct_index=1,
        explanation="Use equal distances, say 120 km each. Times are 2 h and 3 h. Total 240 km in 5 h = 48 km/h.",
        skeleton="average speed = total distance / total time; equal-distance speeds use a harmonic, not arithmetic, average.",
        trap="Taking (60 + 40)/2 = 50.",
        difficulty=3,
        likely_error_if_wrong=ErrorCause.TRAP_SELECTED,
    ),
    Question(
        id="Q-SET-001",
        section=Section.QUANT,
        archetype_id="Q_OVERLAP",
        archetype_name="Overlapping sets",
        skill_ids=("set_overlap",),
        prompt="In a group, 60 people like tea, 50 like coffee, and 20 like both. How many like at least one of the two?",
        options=("70", "80", "90", "100", "110"),
        correct_index=2,
        explanation="Tea or coffee = 60 + 50 - 20 = 90. The overlap was counted twice, so subtract it once.",
        skeleton="A ∪ B = A + B - overlap.",
        trap="Adding both groups without correcting the double-counted overlap.",
        difficulty=2,
        likely_error_if_wrong=ErrorCause.CONSTRAINT_MISSED,
    ),
    Question(
        id="Q-INEQ-001",
        section=Section.QUANT,
        archetype_id="Q_ALG_LINEAR",
        archetype_name="Linear inequalities",
        skill_ids=("linear_inequality",),
        prompt="If 2x + 3 > 11, which statement must be true?",
        options=("x > 3", "x > 4", "x < 4", "x ≥ 4", "x < 7"),
        correct_index=1,
        explanation="2x > 8, so x > 4.",
        skeleton="solve like a linear equation; reverse the inequality only when multiplying or dividing by a negative.",
        trap="Confusing > with ≥ or flipping the sign when no negative division occurred.",
        difficulty=1,
        likely_error_if_wrong=ErrorCause.EXECUTION_LOGIC,
    ),
)


QUESTION_BY_ID = {q.id: q for q in SEED_QUESTIONS}
