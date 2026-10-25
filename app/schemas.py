from pydantic import BaseModel, Field, HttpUrl

class CreateUrlRequest(BaseModel):
    url: HttpUrl

class CreateUrlResponse(BaseModel):
    shortCode: str
    originalUrl: str
    shortUrl: str
    createdAtUtc: str

class AnalyticsResponse(BaseModel):
    shortCode: str
    originalUrl: str
    clickCount: int
    createdAtUtc: str
    lastAccessedAtUtc: str | None

class RequirementRequest(BaseModel):
    requirement: str = Field(min_length=8, max_length=5000)
    scenario_type: str | None = Field(default=None, pattern="^(greenfield|brownfield|ambiguous)$")

class RequirementAnalysisResponse(BaseModel):
    requirement: str
    scenario_type: str
    engineering_problem: str
    assumptions: list[str]
    ambiguities: list[str]
    tasks: list[dict]
    validation_checks: list[str]
    risks: list[dict]
    ai_assistance: list[dict]
    note: str
