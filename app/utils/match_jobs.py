from app.tools.job_fetch import fetch_job_tool
from app.schema.graph_schema import ResumeState
from app.schema.model_output_schema import MatchJobOutput
from app.llm.provider import create_llm
from rich import print

def match_jobs(state: ResumeState) -> ResumeState:
    job_availabe = fetch_job_tool()
    model = create_llm()

    structured_model = model.with_structured_output(MatchJobOutput)

    message = [
        {
            "role": "system",
            "content": "You are an expert job matching assistant. Given a candidate's skills and a list of available jobs, rank the jobs by how well they match the candidate's skills. You must always return at least one matched job from the provided list, even if the match is only partial — never return an empty result."
        },
        {
            "role": "user",
            "content": f"""Candidate skills: {state['skills']}
Candidate resume score: {state['overall_score']}

Available jobs (you must choose only from this list):
{job_availabe}
"""
        }
    ]
    res = structured_model.invoke(message)

    return res.model_dump()


    