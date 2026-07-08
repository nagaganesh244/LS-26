from langgraph.graph import StateGraph, END
from state import AgentState
from agents.resume_optimizer import optimize_resume
from agents.ats_evaluator import evaluate_ats
from agents.career_coach import coach_career

def route_evaluation(state: AgentState) -> str:
    """
    Conditional routing logic:
    If ATS score is below 80 AND we haven't optimized 3 times, rewrite again.
    Otherwise, proceed to the career coach.
    """
    if state["ats_score"] < 80 and state["iteration_count"] < 3:
        return "optimize"
    return "coach"

def create_workflow() -> StateGraph:
    """
    Builds and compiles the LangGraph StateGraph.
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("optimizer", optimize_resume)
    workflow.add_node("evaluator", evaluate_ats)
    workflow.add_node("coach", coach_career)
    
    # Define edges
    workflow.set_entry_point("optimizer")
    workflow.add_edge("optimizer", "evaluator")
    
    # Conditional logic after evaluation
    workflow.add_conditional_edges(
        "evaluator",
        route_evaluation,
        {
            "optimize": "optimizer",
            "coach": "coach"
        }
    )
    
    # Final edge
    workflow.add_edge("coach", END)
    
    return workflow.compile()