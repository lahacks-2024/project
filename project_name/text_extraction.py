import fitz  # PyMuPDF
from docx import Document
import io

def extract_text_from_pdf(file_stream):
    text = ""
    with fitz.open(stream=file_stream, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_stream):
    file_stream.seek(0)  # Ensure you're at the start of the file
    doc = Document(file_stream)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def extract_text(file_stream, file_content_type):
    # Use the content type to determine how to extract text
    if file_content_type == 'application/pdf':
        return extract_text_from_pdf(file_stream)
    elif file_content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(file_stream)
    else:
        raise ValueError(f"Unsupported file type: {file_content_type}")