from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from state import AgentState
from prompts import CAREER_COACH_PROMPT
from utils.gemini import get_gemini_chat

class ProjectSuggestion(BaseModel):
    name: str = Field(description="Project Name")
    difficulty: str = Field(description="Beginner, Intermediate, or Advanced")
    estimated_time: str = Field(description="Estimated Time to complete")
    skills_learned: list[str] = Field(description="List of skills learned")
    why_it_helps: str = Field(description="Why it helps for this specific Job Description")

class InterviewQuestions(BaseModel):
    technical: list[str] = Field(description="3 Technical questions with reasons and sample answers")
    behavioral: list[str] = Field(description="3 Behavioral questions with reasons and sample answers")
    gap_based: list[str] = Field(description="2 Questions addressing gaps in the resume")
    hr: list[str] = Field(description="2 HR screening questions")

class CareerReport(BaseModel):
    resume_match_score: int = Field(description="Overall fit out of 100")
    strong_skills: list[str] = Field(description="Skills the candidate already has")
    missing_skills: list[str] = Field(description="Skills missing from the resume")
    missing_technologies: list[str] = Field(description="Technologies missing from the resume")
    important_gaps: list[str] = Field(description="Critical experience gaps")
    roadmap: list[str] = Field(description="Step-by-step learning roadmap")
    projects: list[ProjectSuggestion] = Field(description="Suggested Portfolio Projects")
    interview_questions: InterviewQuestions = Field(description="Personalized Interview Questions")
    final_summary: str = Field(description="Final application readiness summary")

def coach_career(state: AgentState) -> dict:
    """
    Agent 3: Provides deep career insights and structured interview prep based on the final optimized resume.
    """
    llm = get_gemini_chat("gemini-2.5-flash", temperature=0.3, api_key=state.get("gemini_api_key"))
    structured_llm = llm.with_structured_output(CareerReport)
    
    prompt = PromptTemplate(
        template=CAREER_COACH_PROMPT,
        input_variables=["job_description", "optimized_resume"]
    )
    
    chain = prompt | structured_llm
    report: CareerReport = chain.invoke({
        "job_description": state["job_description"],
        "optimized_resume": state["optimized_resume"]
    })
    
    return {
        "career_report": "Report Generated Successfully.",
        "project_suggestions": [p.dict() for p in report.projects],
        "interview_questions": report.interview_questions.dict(),
        "missing_skills": report.missing_skills,
        "final_summary": report.final_summary
    }