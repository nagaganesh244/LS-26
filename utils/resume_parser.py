import fitz
import base64
from langchain_core.messages import HumanMessage
from utils.gemini import get_gemini_chat

def extract_text_from_pdf(pdf_file, api_key: str | None = None) -> str:
    """
    Extracts plain text from an uploaded PDF file using PyMuPDF.
    Falls back to Gemini 2.5 Flash for image-based or scanned PDFs.
    """
    text = ""
    try:
        pdf_bytes = pdf_file.getvalue()
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text() + "\n"
    except Exception as e:
        pass
        
    text = text.strip()
    if len(text) > 50:
        return text

    # Fallback to Gemini for scanned PDFs
    try:
        pdf_bytes = pdf_file.getvalue()
        encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        
        llm = get_gemini_chat("gemini-2.5-flash", api_key=api_key)
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "Extract all the readable text from this document. Preserve the structure, sections, and formatting as much as possible.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:application/pdf;base64,{encoded_pdf}"
                    }
                },
            ]
        )
        response = llm.invoke([message])
        if response.content:
            text = response.content.strip()
    except Exception as e:
        raise ValueError(f"Gemini fallback failed: {str(e)}")
        
    return text