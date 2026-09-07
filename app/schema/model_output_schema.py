from pydantic import BaseModel, Field
from typing import List, Optional


class SkillExtractionOutput(BaseModel):
    skills: List[str] = Field(..., description="List of technical and soft skills found in the resume")


class AnalysisOutput(BaseModel):
    overall_score: int = Field(..., ge=0, le=100, description="Overall resume score from 0 to 100")
    recommendation: str = Field(..., description="High-level recommendation for the candidate")
    suggestions: List[str] = Field(..., description="Specific, actionable suggestions to improve the resume")
    verdict: str = Field(..., description="Final verdict summarizing fit, e.g. Strong Fit, Moderate Fit, Weak Fit")

class MatchedJob(BaseModel):
    role: str = Field(..., description="The job role title")
    match_score: int = Field(..., ge=0, le=100, description="How well the resume matches this job, 0-100")

class MatchJobOutput(BaseModel):
    matched_jobs: List[MatchedJob] = Field(..., description="List of jobs ranked by match quality, best first. Always return at least one job from the available list, even if the match is weak.")