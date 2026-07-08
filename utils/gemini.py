import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_gemini_chat(model: str, temperature: float = 0.0, api_key: str | None = None):
    """Create a Gemini chat client using the provided API key or environment fallback."""
    key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("A Gemini API key is required.")
    return ChatGoogleGenerativeAI(model=model, temperature=temperature, api_key=key)
