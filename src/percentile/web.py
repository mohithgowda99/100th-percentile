from __future__ import annotations

from datetime import date
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .models import ErrorCause
from .questions import QUESTION_BY_ID, SEED_QUESTIONS
from .storage import Store
from .trainer import SessionMode, build_session, recommend_from_skill_stats


TARGET_DATE = date(2026, 11, 20)
ASSET_DIR = Path(__file__).with_name("web_assets")

app = FastAPI(title="100th Percentile", version="0.2.0")
app.mount("/assets", StaticFiles(directory=ASSET_DIR), name="assets")


def get_store() -> Store:
    return Store()


class AttemptIn(BaseModel):
    question_id: str
    selected_index: int = Field(ge=0)
    response_seconds: float = Field(ge=0)
    confidence: float | None = Field(default=None, ge=0, le=1)
    self_reported_error: ErrorCause | None = None


class RecognitionAttemptIn(BaseModel):
    question_id: str
    selected_archetype_id: str
    response_seconds: float = Field(ge=0)
    confidence: float | None = Field(default=None, ge=0, le=1)


class MockIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    total_score: int | None = Field(default=None, ge=205, le=805)
    quant_score: int | None = Field(default=None, ge=60, le=90)
    verbal_score: int | None = Field(default=None, ge=60, le=90)
    di_score: int | None = Field(default=None, ge=60, le=90)
    notes: str | None = Field(default=None, max_length=2000)


@app.get("/")
def index():
    return FileResponse(ASSET_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"ok": True, "version": app.version}


@app.get("/api/session")
def session(
    mode: SessionMode = SessionMode.FOUNDATION,
    limit: int = Query(default=8, ge=1, le=20),
):
    questions = build_session(mode=mode, limit=limit)
    archetype_choices = [
        {"id": archetype_id, "name": archetype_name}
        for archetype_id, archetype_name in sorted(
            {(q.archetype_id, q.archetype_name) for q in SEED_QUESTIONS}
        )
    ]
    return {
        "mode": mode.value,
        "questions": [
            {
                "id": q.id,
                "section": q.section.value,
                "prompt": q.prompt,
                "options": q.options,
                "difficulty": q.difficulty,
                **({"archetype_choices": archetype_choices} if mode == SessionMode.RECOGNITION else {}),
            }
            for q in questions
        ],
    }


@app.post("/api/attempt")
def attempt(payload: AttemptIn):
    question = QUESTION_BY_ID.get(payload.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Unknown question")
    if payload.selected_index >= len(question.options):
        raise HTTPException(status_code=422, detail="selected_index outside option range")

    correct = payload.selected_index == question.correct_index
    likely_error = None if correct else question.likely_error_if_wrong
    error_to_store = payload.self_reported_error or likely_error

    get_store().save_attempt(
        question_id=question.id,
        selected_index=payload.selected_index,
        correct=correct,
        response_seconds=payload.response_seconds,
        confidence=payload.confidence,
        error_cause=error_to_store,
    )

    return {
        "correct": correct,
        "correct_index": question.correct_index,
        "archetype_id": question.archetype_id,
        "archetype_name": question.archetype_name,
        "skill_ids": question.skill_ids,
        "explanation": question.explanation,
        "skeleton": question.skeleton,
        "trap": question.trap,
        "likely_error": likely_error.value if likely_error else None,
    }


@app.post("/api/recognition-attempt")
def recognition_attempt(payload: RecognitionAttemptIn):
    question = QUESTION_BY_ID.get(payload.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Unknown question")

    correct = payload.selected_archetype_id == question.archetype_id
    get_store().save_recognition_attempt(
        question_id=question.id,
        selected_archetype_id=payload.selected_archetype_id,
        correct=correct,
        response_seconds=payload.response_seconds,
        confidence=payload.confidence,
    )
    return {
        "correct": correct,
        "archetype_id": question.archetype_id,
        "archetype_name": question.archetype_name,
        "skeleton": question.skeleton,
        "trap": question.trap,
        "explanation": question.explanation,
    }


@app.get("/api/dashboard")
def dashboard():
    store = get_store()
    summary = store.attempt_summary()
    recommendations = recommend_from_skill_stats(store.skill_stats())
    return {
        "target_date": TARGET_DATE.isoformat(),
        "days_remaining": max(0, (TARGET_DATE - date.today()).days),
        "summary": summary,
        "recognition": store.recognition_summary(),
        "latest_mock": store.latest_mock(),
        "top_recommendation": (
            {
                "target_id": recommendations[0].target_id,
                "score": round(recommendations[0].score, 3),
                "reason_codes": recommendations[0].reason_codes,
            }
            if recommendations
            else None
        ),
    }


@app.get("/api/recommendations")
def recommendations():
    recs = recommend_from_skill_stats(get_store().skill_stats())
    return [
        {
            "target_id": r.target_id,
            "score": round(r.score, 3),
            "reason_codes": r.reason_codes,
        }
        for r in recs[:8]
    ]


@app.get("/api/atlas")
def atlas():
    by_archetype: dict[str, dict[str, object]] = {}
    for q in SEED_QUESTIONS:
        row = by_archetype.setdefault(
            q.archetype_id,
            {
                "id": q.archetype_id,
                "name": q.archetype_name,
                "question_count": 0,
                "skills": set(),
            },
        )
        row["question_count"] = int(row["question_count"]) + 1
        row["skills"].update(q.skill_ids)  # type: ignore[union-attr]

    return [
        {
            **row,
            "skills": sorted(row["skills"]),
        }
        for row in by_archetype.values()
    ]


@app.post("/api/mock")
def log_mock(payload: MockIn):
    get_store().save_mock(
        name=payload.name,
        total_score=payload.total_score,
        quant_score=payload.quant_score,
        verbal_score=payload.verbal_score,
        di_score=payload.di_score,
        notes=payload.notes,
    )
    return {"ok": True}


def run() -> None:
    import uvicorn

    uvicorn.run("percentile.web:app", host="127.0.0.1", port=8000, reload=True)
