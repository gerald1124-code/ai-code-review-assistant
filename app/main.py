from fastapi import FastAPI
from app.schemas import ReviewRequest, ReviewResponse
from app.reviewer import review_code

app = FastAPI(title="AI Code Review Assistant", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/review", response_model=ReviewResponse)
def review(payload: ReviewRequest):
    score, findings = review_code(payload.code)
    return {
        "filename": payload.filename,
        "score": score,
        "findings": findings,
    }
