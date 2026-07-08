import streamlit as st
import os
from dotenv import load_dotenv
from utils.resume_parser import extract_text_from_pdf
from utils.jd_parser import clean_job_description
from utils.resume_validator import is_resume
from graph import create_workflow

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Resume Enhancer", layout="wide")

def init_session_state():
    if "workflow_running" not in st.session_state:
        st.session_state.workflow_running = False
    if "final_state" not in st.session_state:
        st.session_state.final_state = None

init_session_state()

st.title("Resume Enhancer")
st.markdown("### Multi-Agent Resume Optimization and Career Guidance")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Upload Details")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value="",
        placeholder="Enter your Gemini API key",
        help="Enter your Gemini API key here. It will be used for PDF parsing, validation, and resume optimization."
    )

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    job_description = st.text_area("Paste Job Description", height=200)
    
    analyze_btn = st.button("Analyze & Optimize", type="primary", use_container_width=True)

# --- MAIN LOGIC ---
if analyze_btn:
    if not api_key:
        st.error("Please provide a valid Google Gemini API Key.")
    elif not uploaded_file:
        st.error("Please upload a resume (PDF).")
    elif not job_description:
        st.error("Please paste the Job Description.")
    else:
        st.session_state.workflow_running = True
        
        # Parse inputs
        with st.spinner("Extracting and validating PDF..."):
            # Ensure downstream helpers that still read an env var can find the key.
            # We set it in-process only (no prefill in the UI).
            os.environ["GOOGLE_API_KEY"] = api_key

            # Call the parser/validator without using keyword-style args to
            # remain compatible with any older signatures.
            resume_text = extract_text_from_pdf(uploaded_file)

            if len(resume_text.strip()) < 50:
                st.error("No readable text found in the PDF. Please ensure it is a text-based PDF and not a scanned image.")
                st.stop()

            if not is_resume(resume_text):
                st.error("The uploaded document does not appear to be a valid resume. Please upload a corrected one.")
                st.stop()

            cleaned_jd = clean_job_description(job_description)
            
        st.info("Starting Multi-Agent LangGraph Workflow...")
        
        # Initialize graph
        app = create_workflow()
        
        # Initial State
        initial_state = {
            "resume_text": resume_text,
            "job_description": cleaned_jd,
            "gemini_api_key": api_key,
            "iteration_count": 0,
            "rewrite_history": []
        }
        
        # Run workflow and stream output for UI updates
        final_state = initial_state
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            for output in app.stream(initial_state):
                for node_name, state_update in output.items():
                    final_state.update(state_update)
                    
                    if node_name == "optimizer":
                        status_text.write(f"Optimizer Agent (Iteration {final_state.get('iteration_count', 1)}): Rewriting resume...")
                        progress_bar.progress(30)
                    elif node_name == "evaluator":
                        score = final_state.get('ats_score', 0)
                        status_text.write(f"ATS Evaluator: Scored {score}/100")
                        progress_bar.progress(60)
                    elif node_name == "coach":
                        status_text.write("Career Coach Agent: Generating roadmap & interview prep...")
                        progress_bar.progress(90)
            
            progress_bar.progress(100)
            status_text.success("Workflow Complete!")
            st.session_state.final_state = final_state
        except Exception as e:
            st.error(f"An error occurred during workflow execution: {str(e)}")

# --- RESULTS DASHBOARD ---
if st.session_state.final_state:
    state = st.session_state.final_state
    
    st.divider()
    
    # Top Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Iterations", state.get("iteration_count", 0))
    col2.metric("Overall ATS Score", f"{state.get('ats_score', 0)}/100")
    col3.metric("Keyword Match", f"{state.get('keyword_score', 0)}/100")
    
    # Determine readiness based on score
    score = state.get('ats_score', 0)
    readiness = "Ready to Apply" if score >= 80 else "Needs Work"
    col4.metric("Application Readiness", readiness)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Optimized Resume", "ATS Analysis", "Career Coach", "Interview Prep"])
    
    with tab1:
        st.subheader("Final Optimized Resume")
        st.markdown(state.get("optimized_resume", "No optimized resume generated."))
        st.download_button(
            label="Download Optimized Resume (TXT)",
            data=state.get("optimized_resume", ""),
            file_name="optimized_resume.txt",
            mime="text/plain"
        )
        
    with tab2:
        st.subheader("ATS Feedback")
        c1, c2 = st.columns(2)
        with c1:
            st.success("Matched Keywords")
            for kw in state.get("matched_keywords", []):
                st.write(f"{kw}")
            
            st.info("Strengths")
            for s in state.get("strengths", []):
                st.write(f"• {s}")
                
        with c2:
            st.error("Missing Keywords")
            for kw in state.get("missing_keywords", []):
                st.write(f"{kw}")
                
            st.warning("Weaknesses / Improvement Areas")
            for w in state.get("weaknesses", []):
                st.write(f"• {w}")
                
    with tab3:
        st.subheader("Personalized Career Guidance")
        st.write(f"**Final Summary:** {state.get('final_summary', '')}")
        
        st.markdown("#### Suggested Portfolio Projects to Bridge Gaps")
        for proj in state.get("project_suggestions", []):
            with st.expander(f"{proj.get('name')} ({proj.get('difficulty')})"):
                st.write(f"**Time:** {proj.get('estimated_time')}")
                st.write(f"**Why it helps:** {proj.get('why_it_helps')}")
                st.write(f"**Skills:** {', '.join(proj.get('skills_learned', []))}")
                
    with tab4:
        st.subheader("Personalized Interview Questions")
        questions = state.get("interview_questions", {})
        
        with st.expander("Technical Questions", expanded=True):
            for q in questions.get("technical", []):
                st.markdown(f"- {q}")
                
        with st.expander("Behavioral Questions"):
            for q in questions.get("behavioral", []):
                st.markdown(f"- {q}")
                
        with st.expander("Gap-Based Questions"):
            for q in questions.get("gap_based", []):
                st.markdown(f"- {q}")