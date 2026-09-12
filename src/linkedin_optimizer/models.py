from pydantic import BaseModel, Field


class Profile(BaseModel):
    headline: str = ""
    about: str = ""
    experience: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)


class Role(BaseModel):
    title: str
    description: str = ""


class Signal(BaseModel):
    category: str
    name: str
    score: float = Field(ge=0, le=100)
    evidence: str
    recommendation: str


class OptimizationReport(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    signals: list[Signal]
    matched_keywords: list[str]
    missing_keywords: list[str]
