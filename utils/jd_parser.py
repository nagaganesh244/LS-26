import re

def clean_job_description(jd_text: str) -> str:
    """
    Cleans and normalizes the job description text.
    Removes excessive whitespace and special characters.
    """
    text = re.sub(r'[^\w\s.,;:()-]', '', jd_text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()