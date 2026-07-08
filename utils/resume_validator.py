from langchain_core.prompts import PromptTemplate
from utils.gemini import get_gemini_chat

def is_resume(text: str, api_key: str | None = None) -> bool:
    """Checks if the given text is likely a resume."""
    llm = get_gemini_chat("gemini-2.5-flash", temperature=0.0, api_key=api_key)
    prompt = PromptTemplate(
        template="""You are an expert recruiter. Read the following text and determine if it is a resume or curriculum vitae (CV). 
If the text contains a person's profile, work history, skills, or educational background, it is a resume. 
Even if it is poorly formatted, missing some sections, or very brief, if it is clearly meant to represent a person's professional profile, respond with exactly 'YES'.
If it is a completely unrelated document (e.g., a legal contract, an invoice, an article, random text, or a job description), respond with exactly 'NO'.
Do not provide any other text or explanation.

Text:
{text}
""",
        input_variables=["text"]
    )
    chain = prompt | llm
    response = chain.invoke({"text": text[:5000]})
    
    return "YES" in response.content.strip().upper()
