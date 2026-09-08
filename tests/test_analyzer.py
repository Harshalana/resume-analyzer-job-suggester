"""
CareerCraft AI - Automated Test Suite
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.parser import parse_resume, extract_contact_info, extract_skills, split_sections
from backend.scorer import evaluate_resume
from backend.job_matcher import suggest_jobs_for_resume, match_custom_job_description
from backend.generator import generate_tailored_cover_letter, generate_interview_prep
from backend.samples import SAMPLE_RESUMES

client = TestClient(app)


def test_health_check():
    """Verify health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_sample_resumes():
    """Verify sample resumes list."""
    response = client.get("/api/sample-resumes")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 5
    assert samples[0]["name"] == "Alex Morgan"


def test_get_market_jobs():
    """Verify market roles retrieval & filter."""
    response = client.get("/api/jobs")
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) >= 8

    # Test filtering by category
    filtered = client.get("/api/jobs?category=Software Engineering")
    assert filtered.status_code == 200
    assert all(j["category"] == "Software Engineering" for j in filtered.json())


def test_resume_parser_extraction():
    """Test contact extraction, skill tagging, and sections."""
    sample_text = SAMPLE_RESUMES[0]["text"]
    parsed = parse_resume(sample_text)

    assert parsed["contact"]["name"] == "Alex Morgan"
    assert parsed["contact"]["email"] == "alex.morgan@example.com"
    assert "github.com" in parsed["contact"]["github"]
    assert "linkedin.com" in parsed["contact"]["linkedin"]

    skills = parsed["skills"]
    assert skills["total_count"] >= 10
    assert "react" in skills["all_skills"]
    assert "docker" in skills["all_skills"]
    assert "typescript" in skills["all_skills"]

    assert "experience" in parsed["sections"]
    assert "skills" in parsed["sections"]
    assert len(parsed["bullets"]) >= 4
    assert len(parsed["action_verbs"]) >= 3


def test_scorer_evaluation():
    """Test ATS scoring and sub-score metrics."""
    sample_text = SAMPLE_RESUMES[0]["text"]
    parsed = parse_resume(sample_text)
    eval_res = evaluate_resume(parsed)

    assert eval_res["overall_score"] >= 75
    assert "sub_scores" in eval_res
    assert len(eval_res["strengths"]) > 0
    assert eval_res["metrics_summary"]["total_skills"] >= 10


def test_job_matcher():
    """Test job suggestion engine."""
    sample_text = SAMPLE_RESUMES[0]["text"]
    parsed = parse_resume(sample_text)
    job_matches = suggest_jobs_for_resume(parsed)

    assert len(job_matches) > 0
    # Alex Morgan is a Senior Full-Stack Engineer, so Full-Stack should be a top match
    top_match = job_matches[0]
    assert "Full-Stack" in top_match["title"] or top_match["match_percentage"] >= 75
    assert len(top_match["matched_skills"]) > 0


def test_custom_jd_matcher():
    """Test matching against a custom job description."""
    sample_text = SAMPLE_RESUMES[0]["text"]
    parsed = parse_resume(sample_text)

    custom_jd = """
    We are looking for a Senior React & Node.js Engineer with experience in AWS, TypeScript, and Docker.
    Knowledge of Kubernetes and GraphQL is a strong plus.
    """
    jd_match = match_custom_job_description(parsed, custom_jd)

    assert jd_match["job_match_score"] >= 60
    assert "React" in jd_match["matched_skills"]
    assert len(jd_match["tailoring_recommendations"]) > 0


def test_cover_letter_generator():
    """Test cover letter generation."""
    letter = generate_tailored_cover_letter(
        candidate_name="Alex Morgan",
        contact_info={"email": "alex@example.com", "phone": "555-1234"},
        skills=["React", "TypeScript", "Node.js"],
        experience_summary="Senior Engineer",
        job_title="Lead Software Engineer",
        company_name="Acme Inc."
    )
    assert "Alex Morgan" in letter
    assert "Acme Inc." in letter
    assert "React" in letter


def test_interview_prep_generator():
    """Test interview questions generation."""
    questions = generate_interview_prep(
        candidate_skills=["React", "Docker", "AWS"],
        job_title="Senior Developer",
        missing_skills=["Kubernetes"]
    )
    assert len(questions) == 5
    assert any("Kubernetes" in q["question"] or "Kubernetes" in q.get("tip", "") for q in questions)


def test_api_analyze_endpoint():
    """Test full analyze endpoint over HTTP."""
    sample_text = SAMPLE_RESUMES[1]["text"] # Sophia Chen (AI/ML)
    response = client.post("/api/analyze", data={"text": sample_text})

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert res_json["parsed"]["contact"]["name"] == "Dr. Sophia Chen"
    assert res_json["evaluation"]["overall_score"] >= 75
    assert "AI & Machine Learning Engineer" in [j["title"] for j in res_json["job_matches"][:3]]

