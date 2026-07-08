from typing import List

def calculate_ats_score(matched_keywords: List[str], total_keywords: int, resume_text: str) -> dict:
    """
    Calculates the ATS Score based on keyword coverage, action verbs, and length heuristics.
    """
    if total_keywords == 0:
        return {"ats_score": 0, "keyword_score": 0}
        
    # 1. Keyword Coverage (60% weight)
    keyword_ratio = len(matched_keywords) / total_keywords
    keyword_score = int(keyword_ratio * 100)
    
    # 2. Action Verb Heuristic (20% weight)
    action_verbs = ['achieved', 'developed', 'managed', 'created', 'led', 'designed', 'improved', 'increased', 'reduced', 'implemented']
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    verb_score = min(100, verb_count * 10) # 10 points per verb, max 100
    
    # 3. Length / Detail Heuristic (20% weight)
    # Assume a good resume is between 1500 and 4000 characters
    char_count = len(resume_text)
    if 1500 <= char_count <= 4000:
        length_score = 100
    elif char_count > 4000:
        length_score = 80 # Slightly penalized for being too long
    else:
        length_score = max(0, int((char_count / 1500) * 100)) # Penalized for being too short
        
    # Calculate weighted total
    overall_score = int((keyword_score * 0.6) + (verb_score * 0.2) + (length_score * 0.2))
    
    return {
        "ats_score": overall_score,
        "keyword_score": keyword_score
    }