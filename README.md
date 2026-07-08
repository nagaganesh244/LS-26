# Resume Enhancer

Resume Enhancer is a Streamlit-based application that helps job seekers improve their resume for a specific job description using a multi-agent workflow powered by LangGraph and Google Gemini.

## What it does

The app:
- Uploads a resume PDF
- Accepts a job description
- Extracts and validates resume content
- Uses a multi-agent workflow to:
  - rewrite the resume for ATS and relevance
  - evaluate keyword coverage and ATS fit
  - generate career coaching, project suggestions, and interview prep questions

## Tech stack

- Python
- Streamlit for the web UI
- LangGraph for the multi-agent workflow
- LangChain + Google Gemini for AI-powered rewriting and evaluation
- Pydantic for structured output models

## Project structure

- app.py — Streamlit application entry point
- graph.py — LangGraph workflow definition
- state.py — Shared workflow state schema
- prompts.py — Prompt templates for the agents
- agents/ — Agent implementations
  - resume_optimizer.py
  - ats_evaluator.py
  - career_coach.py
- utils/ — Resume parsing, validation, keyword matching, scoring, and Gemini helpers

## Prerequisites

- Python 3.10+
- A Google Gemini API key

## Installation

1. Open the project folder
2. Create and activate a virtual environment (recommended)
3. Install the required dependencies:

```bash
pip install streamlit python-dotenv langgraph langchain-core langchain-google-genai pydantic
```

## Environment setup

Set your Gemini API key as an environment variable:

On Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

Or create a .env file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run the app

From the project root, run:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## How to use it

1. Enter your Gemini API key
2. Upload a resume PDF
3. Paste the target job description
4. Click "Analyze & Optimize"
5. Review the optimized resume, ATS analysis, and coaching insights

## Notes

- The uploaded resume should be a text-based PDF for best results
- The app does not fabricate experience or skills; it rewrites existing content to better match the job description
- The workflow may take some time depending on the size of the resume and the API response time
