"""
CareerCraft AI - FastAPI Web Application & REST API
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    parse_resume
)
from backend.scorer import evaluate_resume
from backend.job_matcher import suggest_jobs_for_resume, match_custom_job_description
from backend.generator import generate_tailored_cover_letter, generate_interview_prep
from backend.samples import SAMPLE_RESUMES
from backend.taxonomy import MARKET_JOB_ROLES

app = FastAPI(
    title="CareerCraft AI - Resume Analyzer & Job Suggester",
    description="Intelligent ATS scoring, skill gap analysis, job matching, and career tools",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Request Models
class AnalyzeTextRequest(BaseModel):
    text: str

class CustomJDMatchRequest(BaseModel):
    resume_text: str
    job_description: str

class CoverLetterRequest(BaseModel):
    candidate_name: Optional[str] = "Candidate"
    contact_info: Optional[Dict[str, Any]] = {}
    skills: Optional[List[str]] = []
    job_title: str
    company_name: Optional[str] = "Hiring Team"
    experience_summary: Optional[str] = ""

class InterviewPrepRequest(BaseModel):
    skills: List[str]
    job_title: str
    missing_skills: Optional[List[str]] = []


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "CareerCraft AI"}


@app.get("/api/sample-resumes")
async def get_sample_resumes():
    """Retrieve curated sample resumes for instant exploration."""
    return SAMPLE_RESUMES


@app.get("/api/jobs")
async def get_market_jobs(category: Optional[str] = None, level: Optional[str] = None):
    """Retrieve catalog of market roles with optional filtering."""
    roles = MARKET_JOB_ROLES
    if category:
        roles = [r for r in roles if r.get("category", "").lower() == category.lower()]
    if level:
        roles = [r for r in roles if level.lower() in r.get("level", "").lower()]
    return roles


@app.post("/api/analyze")
async def analyze_resume_endpoint(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Analyze resume from uploaded file (PDF, DOCX, TXT) or raw pasted text.
    Returns complete parsed details, ATS score, and recommended jobs.
    """
    raw_text = ""

    if file:
        filename = file.filename.lower()
        contents = await file.read()
        
        if filename.endswith(".pdf"):
            try:
                raw_text = extract_text_from_pdf(contents)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to read PDF: {str(e)}")
        elif filename.endswith((".docx", ".doc")):
            try:
                raw_text = extract_text_from_docx(contents)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to read DOCX: {str(e)}")
        elif filename.endswith(".txt") or filename.endswith(".md"):
            try:
                raw_text = contents.decode("utf-8", errors="ignore")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to read text file: {str(e)}")
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a PDF, DOCX, or plain text file."
            )
    elif text and text.strip():
        raw_text = text.strip()
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide a resume file or paste resume text."
        )

    if not raw_text.strip() or len(raw_text.strip().split()) < 15:
        raise HTTPException(
            status_code=400,
            detail="Resume content is too short or could not be extracted. Please ensure the file contains legible text."
        )

    # 1. Parse Resume
    parsed_data = parse_resume(raw_text)

    # 2. Score Resume for ATS & Impact
    evaluation = evaluate_resume(parsed_data)

    # 3. Match against Market Roles
    job_matches = suggest_jobs_for_resume(parsed_data)

    return {
        "success": True,
        "parsed": parsed_data,
        "evaluation": evaluation,
        "job_matches": job_matches
    }


@app.post("/api/match-custom-jd")
async def match_custom_jd_endpoint(request: CustomJDMatchRequest):
    """Compare candidate resume against a specific custom job description."""
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description text is required.")

    parsed_resume = parse_resume(request.resume_text)
    jd_analysis = match_custom_job_description(parsed_resume, request.job_description)

    # Generate tailored interview questions based on match results
    interview_questions = generate_interview_prep(
        candidate_skills=jd_analysis.get("matched_skills", []),
        job_title="Target Position",
        missing_skills=jd_analysis.get("missing_skills", [])
    )

    return {
        "success": True,
        "match_analysis": jd_analysis,
        "interview_prep": interview_questions
    }


@app.post("/api/generate-cover-letter")
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    """Generate tailored cover letter."""
    cover_letter = generate_tailored_cover_letter(
        candidate_name=request.candidate_name or "Candidate",
        contact_info=request.contact_info or {},
        skills=request.skills or [],
        experience_summary=request.experience_summary or "",
        job_title=request.job_title,
        company_name=request.company_name or "Hiring Team"
    )
    return {"success": True, "cover_letter": cover_letter}


@app.post("/api/generate-interview-prep")
async def generate_interview_prep_endpoint(request: InterviewPrepRequest):
    """Generate tailored interview questions with STAR answers."""
    questions = generate_interview_prep(
        candidate_skills=request.skills,
        job_title=request.job_title,
        missing_skills=request.missing_skills or []
    )
    return {"success": True, "questions": questions}


# Mount Static Frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

