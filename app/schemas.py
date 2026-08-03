from pydantic import BaseModel, Field

class ReviewRequest(BaseModel):
    filename: str = Field(default="snippet.py")
    code: str

class Finding(BaseModel):
    rule: str
    severity: str
    line: int
    message: str
    suggestion: str

class ReviewResponse(BaseModel):
    filename: str
    score: int
    findings: list[Finding]
