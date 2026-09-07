from typing import TypedDict, List, Optional

class ResumeState(TypedDict):
    raw_text: str
    skills: Optional[List[str]]
    overall_score: Optional[int]
    recommendation: Optional[str]
    suggestions: Optional[List[str]]
    verdict: Optional[str]
    matched_jobs: Optional[list]