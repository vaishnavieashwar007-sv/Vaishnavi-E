from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="EduGenie AI",
    version="1.0.0",
    description=(
        "AI-powered educational assistant for "
        "Q&A, explanations, quizzes, summaries "
        "and personalized learning paths."
    ),
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# =========================================================
# REQUEST MODELS
# =========================================================

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"

    weeks: int = Field(
        default=6,
        ge=1,
        le=52
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "message": "EduGenie AI is running"
    }


# =========================================================
# Q&A
# =========================================================

@app.post("/qa")
async def qa(payload: QuestionRequest):

    try:

        result = answer_question(
            payload.question
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print(
            "Q&A ERROR:",
            repr(e)
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# EXPLAIN CONCEPT
# =========================================================

@app.post("/explain")
async def explain(payload: TextRequest):

    try:

        result = explain_topic(
            payload.text
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print(
            "EXPLAIN ERROR:",
            repr(e)
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# QUIZ
# =========================================================

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    try:

        result = generate_quiz(
            payload.text,
            payload.count
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print(
            "QUIZ ERROR:",
            repr(e)
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# SUMMARY
# =========================================================

@app.post("/summarize")
async def summarize(payload: TextRequest):

    try:

        result = summarize_text(
            payload.text
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        print(
            "SUMMARY ERROR:",
            repr(e)
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# PERSONALIZED LEARNING PATH
# =========================================================

@app.post("/learn/recommendations")
async def recommendations(
    payload: LearningPathRequest
):

    try:

        result = get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.weeks
        )

        return {
            "success": True,
            "result": result
        }

    except TypeError:

        # Compatibility fallback if learning_path.py
        # accepts only topic and level.

        try:

            result = get_learning_recommendations(
                payload.topic,
                payload.level
            )

            return {
                "success": True,
                "result": result
            }

        except Exception as e:

            print(
                "LEARNING PATH ERROR:",
                repr(e)
            )

            return {
                "success": False,
                "error": str(e)
            }

    except Exception as e:

        print(
            "LEARNING PATH ERROR:",
            repr(e)
        )

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )