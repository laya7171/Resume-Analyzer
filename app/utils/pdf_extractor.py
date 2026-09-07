from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file given its bytes representation"""
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()
