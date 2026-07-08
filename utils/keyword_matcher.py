import re
from typing import List, Tuple

def normalize_word(word: str) -> str:
    """Lowercases and strips punctuation from a word."""
    return re.sub(r'[^\w]', '', word.lower().strip())

def match_keywords(resume_text: str, jd_keywords: List[str]) -> Tuple[List[str], List[str]]:
    """
    Checks which JD keywords exist in the resume text using string matching.
    Returns (matched_keywords, missing_keywords).
    """
    matched = []
    missing = []
    
    resume_normalized = resume_text.lower()
    
    for kw in jd_keywords:
        kw_clean = kw.strip()
        if not kw_clean:
            continue
            
        # Check if the keyword (lowercased) exists in the normalized resume
        if kw_clean.lower() in resume_normalized:
            matched.append(kw_clean)
        else:
            missing.append(kw_clean)
            
    return matched, missing