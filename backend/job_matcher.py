"""
CareerCraft AI - Job Matching, Skill Gap Analysis & Custom JD Comparator
"""

from typing import Dict, List, Any, Set
from backend.taxonomy import MARKET_JOB_ROLES, SKILL_TAXONOMY, CANONICAL_SKILL_MAP
from backend.parser import extract_skills


def calculate_job_match(candidate_skills: Set[str], role: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate match score and skill gaps between candidate and a target role."""
    required = set(role.get("required_skills", []))
    bonus = set(role.get("bonus_skills", []))

    # Normalize candidate skills to canonical lowercase
    norm_candidate = set(CANONICAL_SKILL_MAP.get(s.lower(), s.lower()) for s in candidate_skills)
    
    # Map required & bonus skills through canonical map
    norm_required = set(CANONICAL_SKILL_MAP.get(s.lower(), s.lower()) for s in required)
    norm_bonus = set(CANONICAL_SKILL_MAP.get(s.lower(), s.lower()) for s in bonus)

    matched_required = norm_required.intersection(norm_candidate)
    missing_required = norm_required - norm_candidate

    matched_bonus = norm_bonus.intersection(norm_candidate)
    missing_bonus = norm_bonus - norm_candidate

    # Weighted match formula (Required skills 75%, Bonus skills 25%)
    req_score = (len(matched_required) / len(norm_required)) if norm_required else 1.0
    bon_score = (len(matched_bonus) / len(norm_bonus)) if norm_bonus else 0.5
    
    match_percentage = int((req_score * 75) + (bon_score * 25))
    match_percentage = max(15, min(100, match_percentage))

    # Categorize match suitability
    if match_percentage >= 80:
        fit_level = "High Match (Ready to Apply)"
        badge_color = "emerald"
    elif match_percentage >= 55:
        fit_level = "Moderate Match (Minor Skill Gap)"
        badge_color = "amber"
    else:
        fit_level = "Growth Opportunity (Needs Upskilling)"
        badge_color = "slate"

    return {
        "id": role["id"],
        "title": role["title"],
        "category": role["category"],
        "level": role["level"],
        "experience_years": role["experience_years"],
        "salary_range": role["salary_range"],
        "demand": role["demand"],
        "description": role["description"],
        "match_percentage": match_percentage,
        "fit_level": fit_level,
        "badge_color": badge_color,
        "matched_skills": sorted([s.title() for s in matched_required.union(matched_bonus)]),
        "missing_required": sorted([s.title() for s in missing_required]),
        "missing_bonus": sorted([s.title() for s in missing_bonus]),
        "learning_roadmap": role.get("learning_roadmap", [])
    }


def suggest_jobs_for_resume(parsed_resume: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Match resume against entire catalog of market roles and rank by compatibility."""
    candidate_skills = set(parsed_resume.get("skills", {}).get("all_skills", []))
    
    # Also extract any other skills present in raw text
    all_matched_roles = []
    for role in MARKET_JOB_ROLES:
        role_result = calculate_job_match(candidate_skills, role)
        all_matched_roles.append(role_result)

    # Sort descending by match percentage
    all_matched_roles.sort(key=lambda x: x["match_percentage"], reverse=True)
    return all_matched_roles


def match_custom_job_description(parsed_resume: Dict[str, Any], job_description_text: str) -> Dict[str, Any]:
    """Compare candidate resume directly against a custom job description pasted by the user."""
    candidate_skills = set(parsed_resume.get("skills", {}).get("all_skills", []))
    norm_candidate = set(CANONICAL_SKILL_MAP.get(s.lower(), s.lower()) for s in candidate_skills)
    
    # Extract skills present in the target job description
    jd_skills_data = extract_skills(job_description_text)
    jd_skills = set(jd_skills_data.get("all_skills", []))
    norm_jd_skills = set(CANONICAL_SKILL_MAP.get(s.lower(), s.lower()) for s in jd_skills)

    if not norm_jd_skills:
        # Fallback if no specific tech skills recognized: simple keyword overlap
        words = set(re.findall(r'\b[A-Za-z]{3,}\b', job_description_text.lower()))
        common = words.intersection(norm_candidate)
        match_score = min(85, max(30, int(len(common) / max(len(norm_candidate), 1) * 100)))
        matched = [w.title() for w in common]
        missing = [w.title() for w in list(words)[:8] if w not in norm_candidate]
    else:
        matched_set = norm_jd_skills.intersection(norm_candidate)
        missing_set = norm_jd_skills - norm_candidate
        
        match_score = int((len(matched_set) / len(norm_jd_skills)) * 100)
        match_score = max(10, min(100, match_score))
        
        matched = sorted([s.title() for s in matched_set])
        missing = sorted([s.title() for s in missing_set])

    # Recommendations for tailoring resume to this specific JD
    tailored_tips = []
    if missing:
        tailored_tips.append(f"Add projects or experience highlighting: {', '.join(missing[:4])}.")
    tailored_tips.append("Align your summary section to mirror the primary role title and core responsibilities.")
    tailored_tips.append("Incorporate specific terminology and methodologies mentioned in the job posting.")

    return {
        "job_match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "total_jd_skills_found": len(norm_jd_skills),
        "total_matched": len(matched),
        "tailoring_recommendations": tailored_tips
    }

