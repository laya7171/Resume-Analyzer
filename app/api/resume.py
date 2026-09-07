from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_extractor import extract_text_from_pdf
from app.schema.graph_schema import ResumeState
router = APIRouter()
from app.graph.workflow import workflow

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    file_bytes = await file.read()
    resume_text = extract_text_from_pdf(file_bytes)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Failed to extract text from the PDF file.")



    resume_state: ResumeState = {
    "raw_text": resume_text,
    "skills": None,
    "overall_score": None,
    "recommendation": None,
    "suggestions": None,
    "verdict": None,
    "matched_jobs": None,
}

    final_state = workflow.invoke(resume_state)

    return final_state