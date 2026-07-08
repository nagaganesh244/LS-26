import json
from langchain_core.prompts import PromptTemplate
from state import AgentState
from prompts import ATS_KEYWORD_EXTRACTION_PROMPT, ATS_EXPLANATION_PROMPT
from utils.keyword_matcher import match_keywords
from utils.score_calculator import calculate_ats_score
from utils.gemini import get_gemini_chat

def evaluate_ats(state: AgentState) -> dict:
    """
    Agent 2: Evaluates the optimized resume using Python logic + LLM explanations.
    """
    llm = get_gemini_chat("gemini-2.5-flash", temperature=0.1, api_key=state.get("gemini_api_key"))
    
    kw_prompt = PromptTemplate(
        template=ATS_KEYWORD_EXTRACTION_PROMPT,
        input_variables=["job_description"]
    )
    kw_chain = kw_prompt | llm
    kw_response = kw_chain.invoke({"job_description": state["job_description"]})
    
    jd_keywords = [kw.strip() for kw in kw_response.content.split(',') if kw.strip()]
    
    current_resume = state["optimized_resume"]
    matched_kw, missing_kw = match_keywords(current_resume, jd_keywords)
    
    scores = calculate_ats_score(matched_kw, len(jd_keywords), current_resume)
    
    exp_prompt = PromptTemplate(
        template=ATS_EXPLANATION_PROMPT,
        input_variables=["ats_score", "keyword_score", "matched_keywords", "missing_keywords"]
    )
    exp_chain = exp_prompt | llm
    
    try:
        exp_response = exp_chain.invoke({
            "ats_score": scores["ats_score"],
            "keyword_score": scores["keyword_score"],
            "matched_keywords": ", ".join(matched_kw),
            "missing_keywords": ", ".join(missing_kw)
        })
        
        raw_json = exp_response.content.replace('```json', '').replace('```', '').strip()
        analysis = json.loads(raw_json)
        strengths = analysis.get("strengths", [])
        weaknesses = analysis.get("weaknesses", [])
    except Exception:
        strengths = ["Resume structure is standard."]
        weaknesses = ["Failed to generate specific weakness analysis due to formatting error."]

    return {
        "ats_score": scores["ats_score"],
        "keyword_score": scores["keyword_score"],
        "matched_keywords": matched_kw,
        "missing_keywords": missing_kw,
        "strengths": strengths,
        "weaknesses": weaknesses
    }