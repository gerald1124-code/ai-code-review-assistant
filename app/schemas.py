"""Pydantic request and response schemas."""

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    """Code review request."""

    code: str = Field(
        ...,
        min_length=1,
        description="Python source code to review.",
        examples=["def add(a, b):\n    return a + b"],
    )


class FindingResponse(BaseModel):
    """One static-analysis finding."""

    rule: str
    message: str
    line: int
    severity: str
    deduction: int


class ReviewResponse(BaseModel):
    """Code review response."""

    score: int
    findings: list[FindingResponse]