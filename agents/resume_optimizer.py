from langchain_core.prompts import PromptTemplate
from state import AgentState
from prompts import RESUME_OPTIMIZER_PROMPT
from utils.gemini import get_gemini_chat

def optimize_resume(state: AgentState) -> dict:
    """
    Agent 1: Rewrites the resume to align with the JD without fabricating info.
    """
    llm = get_gemini_chat("gemini-2.5-flash", temperature=0.2, api_key=state.get("gemini_api_key"))
    
    prompt = PromptTemplate(
        template=RESUME_OPTIMIZER_PROMPT,
        input_variables=["job_description", "resume_text"]
    )
    
    current_resume = state.get("optimized_resume") or state["resume_text"]
    
    chain = prompt | llm
    response = chain.invoke({
        "job_description": state["job_description"],
        "resume_text": current_resume
    })
    
    optimized_text = response.content.strip()
    current_iter = state.get("iteration_count", 0) + 1
    
    return {
        "optimized_resume": optimized_text,
        "iteration_count": current_iter,
        "rewrite_history": [f"Iteration {current_iter} completed."]
    }