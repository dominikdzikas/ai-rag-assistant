from pypdf import PdfReader
from io import BytesIO


def extract_text_from_pdf(content: bytes) -> tuple[str, int]:
    reader = PdfReader(BytesIO(content))
    
    pages_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if text.strip():
            pages_text.append(text.strip())
    
    full_text = "\n\n".join(pages_text)
    
    return full_text, len(reader.pages)

