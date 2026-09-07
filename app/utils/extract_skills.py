from app.llm.provider import create_llm
import json
from app.schema.model_output_schema import SkillExtractionOutput


def extract_skills_from_text(text: str) -> list:
    """Extracts skills from the given text using a language model and returns a list of skills."""

    model = create_llm()
    structured_model = model.with_structured_output(SkillExtractionOutput)

    message = [
        {
            "role": "system",
            "content": "Extract skills from the resume text provided by the user. Don't include anything else, only use skills explicitly mentioned in the text. Do not make anything up."
        },
        {
            "role": "user",
            "content": text  # <-- the actual resume text goes here
        }
    ]
    
    result = structured_model.invoke(message)
    return result.skills
