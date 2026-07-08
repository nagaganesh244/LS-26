from typing import List


def calculate_ats_score(matched_keywords: List[str], total_keywords: int, resume_text: str) -> dict:
    """
    Calculates a more balanced ATS score based on keyword coverage,
    action verbs, and resume depth.
    """
    if total_keywords == 0:
        return {"ats_score": 0, "keyword_score": 0}

    keyword_score = int((len(matched_keywords) / total_keywords) * 100)

    action_verbs = ['achieved', 'developed', 'managed', 'created', 'led', 'designed', 'improved', 'increased', 'reduced', 'implemented']
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    verb_bonus = min(15, verb_count * 5)

    char_count = len(resume_text)
    if 1500 <= char_count <= 4000:
        length_bonus = 15
    elif char_count > 4000:
        length_bonus = 10
    else:
        length_bonus = max(0, min(10, int((char_count / 1500) * 10)))

    overall_score = min(100, keyword_score + verb_bonus + length_bonus)

    return {
        "ats_score": overall_score,
        "keyword_score": keyword_score
    }