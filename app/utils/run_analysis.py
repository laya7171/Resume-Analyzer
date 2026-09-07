from app.llm.provider import create_llm
from app.schema.model_output_schema import AnalysisOutput
from rich import print


def run_analysis(resume_text: str, skills: list, job_data: dict = None) -> dict:
    """
    Analyzes the resume against extracted skills (and optionally a matched job)
    and returns a structured score, recommendation, suggestions, and verdict.
    """
 
    model = create_llm()
    structured_model = model.with_structured_output(AnalysisOutput)
 
    skills_str = ", ".join(skills) if skills else "No skills extracted"
 
    job_context = ""
    if job_data:
        job_context = f"""
Compare the resume against this target job:
Role: {job_data.get('role', 'N/A')}
Requirements: {job_data.get('requirements', 'N/A')}
Responsibilities: {job_data.get('responsibility', 'N/A')}
"""
 
    system_prompt = """You are an expert resume reviewer and career coach.
Analyze the resume based only on the information provided.
Do not make up any experience, skills, or qualifications that are not present.
Give a fair, honest, and constructive assessment.
 
Return:
- overall_score: an integer from 0 to 100 reflecting overall resume quality and fit
- recommendation: a short, high-level recommendation for the candidate
- suggestions: a list of specific, actionable improvements
- verdict: a short final verdict summarizing the fit (e.g. Strong Fit, Moderate Fit, Weak Fit)
"""
 
    user_prompt = f"""Resume text:
{resume_text}
 
Extracted skills:
{skills_str}
{job_context}
"""
 
    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
 
    result: AnalysisOutput = structured_model.invoke(message)
    print(result)
 
    return result.model_dump()

