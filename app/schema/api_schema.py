from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeRequest(BaseModel):
    """
    Request model for resume parsing"""

    resume_text: str = Field(..., description="Extracted text from the uploaded resume")
    role: Optional[str] = Field(None, description="Job roles to compare against, eg. 'Frontend Developer")


class ResumeResponse(BaseModel):
    """
    Response model for resume parsing"""

    overall_score: int = Field(..., ge=0, le=100, description="Score out of 100 ")
    recommendations: str = Field(..., description= "High-level recommendations for the candidate")
    suggestions: List[str] = Field(..., description="Specific actionable suggestions to improve the resume")
    verdict: str = Field(..., description="Final verdict, 'Strong fit, 'Needs Improvement'")
