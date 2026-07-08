import re
from typing import List, Tuple


def normalize_word(word: str) -> str:
    """Lowercases and strips punctuation from a word."""
    return re.sub(r'[^\w]', '', word.lower().strip())


def _stem_word(word: str) -> str:
    """Small stemming helper for simple singular/plural handling."""
    word = normalize_word(word)
    if len(word) <= 4:
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("es") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and len(word) > 4:
        return word[:-1]
    return word


def _tokenize(text: str) -> List[str]:
    return [_stem_word(token) for token in re.split(r'[^a-z0-9]+', text.lower()) if token]


def _keyword_matches(resume_text: str, keyword: str) -> bool:
    keyword_norm = normalize_word(keyword)
    if not keyword_norm:
        return False

    resume_norm = normalize_word(resume_text)
    if keyword_norm in resume_norm:
        return True

    resume_tokens = _tokenize(resume_text)
    keyword_tokens = _tokenize(keyword)
    if not keyword_tokens:
        return False

    if len(keyword_tokens) == 1:
        return keyword_tokens[0] in resume_tokens

    return all(token in resume_tokens for token in keyword_tokens)


def match_keywords(resume_text: str, jd_keywords: List[str]) -> Tuple[List[str], List[str]]:
    """
    Checks which JD keywords exist in the resume text using normalized matching.
    Returns (matched_keywords, missing_keywords).
    """
    matched = []
    missing = []

    for kw in jd_keywords:
        kw_clean = kw.strip()
        if not kw_clean:
            continue

        if _keyword_matches(resume_text, kw_clean):
            matched.append(kw_clean)
        else:
            missing.append(kw_clean)

    return matched, missing