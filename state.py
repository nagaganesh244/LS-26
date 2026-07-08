import operator
from typing import TypedDict, List, Dict, Any, Annotated

class AgentState(TypedDict):
    """
    LangGraph state dictionary holding all variables passed between agents.
    """
    resume_text: str
    job_description: str
    gemini_api_key: str
    optimized_resume: str
    iteration_count: int
    ats_score: int
    keyword_score: int
    missing_keywords: List[str]
    matched_keywords: List[str]
    missing_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    rewrite_history: Annotated[List[str], operator.add]
    career_report: str
    interview_questions: Dict[str, Any]
    project_suggestions: List[Dict[str, Any]]
    final_summary: str