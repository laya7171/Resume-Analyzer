from langgraph.graph import StateGraph, START, END
from app.schema.graph_schema import ResumeState
from app.utils.run_analysis import run_analysis
from app.utils.extract_skills import extract_skills_from_text
from app.utils.match_jobs import match_jobs as match_jobs_util


def extract_skills(state: ResumeState) -> dict:
    text = state["raw_text"]
    skills = extract_skills_from_text(text)
    return {"skills": skills}


def analyze_resume(state: ResumeState) -> dict:
    text = state["raw_text"]
    skills = state["skills"]

    result = run_analysis(text, skills)

    return {
        "overall_score": result["overall_score"],
        "recommendation": result["recommendation"]
    }


def match_jobs(state: ResumeState) -> dict:
    result = match_jobs_util(state)
    return {"matched_jobs": result["matched_jobs"]}

flow = StateGraph(ResumeState)

flow.add_node("Extract_skills_node", extract_skills)
flow.add_node("Analyzer_node", analyze_resume)
flow.add_node("Job_matching_node", match_jobs)

flow.add_edge(START, "Extract_skills_node")
flow.add_edge("Extract_skills_node", "Analyzer_node")
flow.add_edge("Analyzer_node", "Job_matching_node")
flow.add_edge("Job_matching_node", END)

workflow = flow.compile()