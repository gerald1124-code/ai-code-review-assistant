"""FastAPI application for the AI Code Review Assistant."""

from fastapi import FastAPI, HTTPException

from app.reviewer import review_code
from app.schemas import ReviewRequest, ReviewResponse


app = FastAPI(
    title="AI Code Review Assistant",
    description="A lightweight API for reviewing Python source code.",
    version="1.0.0",
)


@app.get("/")
def root() -> dict[str, str]:
    """Return basic API information."""

    return {
        "name": "AI Code Review Assistant",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return API health status."""

    return {"status": "healthy"}


@app.post("/review", response_model=ReviewResponse)
def review(request: ReviewRequest) -> ReviewResponse:
    """Review submitted Python source code."""

    try:
        score, findings = review_code(request.code)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReviewResponse(
        score=score,
        findings=findings,
    )