"""
CareerCraft AI - ATS Scoring & Diagnostic Engine
Evaluates resume quality, impact, ATS friendliness, and provides actionable rewrite suggestions.
"""

from typing import Dict, List, Any
import re


def evaluate_resume(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate overall ATS score, sub-scores, strengths, weaknesses, and bullet rewrites."""
    sections = parsed_data.get("sections", {})
    contact = parsed_data.get("contact", {})
    skills_info = parsed_data.get("skills", {})
    bullets = parsed_data.get("bullets", [])
    word_count = parsed_data.get("word_count", 0)
    action_verbs = parsed_data.get("action_verbs", [])

    strengths = []
    improvements = []
    critical_issues = []

    # -------------------------------------------------------------
    # 1. Section Completeness & Contact Info (20% weight)
    # -------------------------------------------------------------
    section_score = 0
    total_sections_checked = 6
    earned_section_points = 0

    if contact.get("email"):
        earned_section_points += 1
    else:
        critical_issues.append("Missing email address: Recruiters and ATS need a verified contact email.")

    if contact.get("phone"):
        earned_section_points += 0.5
    else:
        improvements.append({"type": "warning", "message": "Missing phone number: Adding a contact number improves callback rates."})

    if contact.get("linkedin") or contact.get("github") or contact.get("portfolio"):
        earned_section_points += 0.5
        strengths.append("Includes online professional presence (LinkedIn/GitHub/Portfolio).")
    else:
        improvements.append({"type": "tip", "message": "Add a LinkedIn profile or GitHub URL to give recruiters quick access to your work."})

    if "experience" in sections:
        earned_section_points += 1
        strengths.append("Well-defined Work Experience section present.")
    else:
        critical_issues.append("Missing Work Experience section header: ATS systems look for standard 'Experience' headings.")

    if "education" in sections:
        earned_section_points += 1
        strengths.append("Education section clearly recognized.")
    else:
        improvements.append({"type": "warning", "message": "Education section is missing or using an unconventional header."})

    if "skills" in sections or skills_info.get("total_count", 0) >= 5:
        earned_section_points += 1
        strengths.append(f"Identified {skills_info.get('total_count', 0)} distinct technical & professional skills.")
    else:
        critical_issues.append("Low skill count or missing dedicated 'Skills' section.")

    if "summary" in sections or "projects" in sections or "certifications" in sections:
        earned_section_points += 1

    section_score = min(100, int((earned_section_points / total_sections_checked) * 100))

    # -------------------------------------------------------------
    # 2. Impact & Action Verbs (25% weight)
    # -------------------------------------------------------------
    impact_score = 0
    quantified_count = sum(1 for b in bullets if b.get("has_metrics"))
    action_verb_bullet_count = sum(1 for b in bullets if b.get("has_action_verb"))
    total_bullets = max(len(bullets), 1)

    quantified_ratio = quantified_count / total_bullets
    action_ratio = action_verb_bullet_count / total_bullets

    if quantified_count >= 4:
        strengths.append(f"Strong quantification: {quantified_count} bullet points contain measurable metrics (%, $, numbers).")
    elif quantified_count > 0:
        improvements.append({"type": "warning", "message": f"Only {quantified_count} bullet point(s) contain measurable metrics. Aim to quantify at least 50% of your achievements using the XYZ formula (Accomplished [X], measured by [Y], by doing [Z])."})
    else:
        improvements.append({"type": "critical", "message": "No measurable metrics found in experience bullets. Add percentages, latency reductions, revenue gains, or user counts to demonstrate tangible impact."})

    if len(action_verbs) >= 6:
        strengths.append(f"High-impact vocabulary: Used {len(action_verbs)} powerful action verbs (e.g. {', '.join(action_verbs[:4])}).")
    else:
        improvements.append({"type": "warning", "message": "Incorporate more decisive action verbs (e.g., 'Spearheaded', 'Architected', 'Streamlined', 'Accelerated') instead of passive phrasing like 'Responsible for' or 'Helped with'."})

    impact_score = min(100, int((quantified_ratio * 55) + (action_ratio * 45) + min(len(action_verbs) * 3, 20)))

    # -------------------------------------------------------------
    # 3. Skill Breadth & Depth (25% weight)
    # -------------------------------------------------------------
    skills_score = 0
    total_skills = skills_info.get("total_count", 0)
    category_count = len(skills_info.get("categorized", {}))

    if total_skills >= 12 and category_count >= 3:
        skills_score = 95
        strengths.append(f"Comprehensive multi-domain skill profile spanning {category_count} categories.")
    elif total_skills >= 8:
        skills_score = 80
        strengths.append(f"Solid core skill set ({total_skills} skills detected).")
    elif total_skills >= 4:
        skills_score = 60
        improvements.append({"type": "warning", "message": "Skill set is somewhat sparse. Add relevant frameworks, databases, cloud tools, or methodologies you have worked with."})
    else:
        skills_score = 35
        critical_issues.append("Very few technical skills identified. Expand your skills section to improve ATS keyword indexing.")

    # -------------------------------------------------------------
    # 4. Length, Brevity & Formatting (15% weight)
    # -------------------------------------------------------------
    length_score = 0
    if 350 <= word_count <= 950:
        length_score = 95
        strengths.append(f"Ideal resume length ({word_count} words), fitting cleanly into a standard 1 to 2-page format.")
    elif word_count < 250:
        length_score = 50
        improvements.append({"type": "warning", "message": f"Resume is very brief ({word_count} words). Elaborate on project details, responsibilities, and system architectures."})
    elif word_count > 1200:
        length_score = 65
        improvements.append({"type": "warning", "message": f"Resume is lengthy ({word_count} words). Consider trimming older or less relevant details to maintain recruiter engagement."})
    else:
        length_score = 80

    # -------------------------------------------------------------
    # 5. Keyword Density & ATS Friendliness (15% weight)
    # -------------------------------------------------------------
    keyword_score = 0
    ats_keywords_count = total_skills + len(action_verbs)
    if ats_keywords_count >= 20:
        keyword_score = 95
        strengths.append("Excellent keyword density for ATS search indexing.")
    elif ats_keywords_count >= 12:
        keyword_score = 80
    else:
        keyword_score = 55
        improvements.append({"type": "warning", "message": "ATS keyword density is below average. Add standard industry terminology and tech stack names."})

    # Weighted Overall Score
    overall_score = int(
        (section_score * 0.20) +
        (impact_score * 0.25) +
        (skills_score * 0.25) +
        (length_score * 0.15) +
        (keyword_score * 0.15)
    )

    # Generate Bullet Point Rewrite Optimizations
    bullet_rewrites = []
    weak_verbs = ["worked on", "helped with", "assisted", "responsible for", "handled", "participated in", "did", "tasked with", "was involved in"]
    
    for b in bullets:
        text = b.get("text", "")
        text_lower = text.lower()
        needs_rewrite = False
        reason = ""

        for wv in weak_verbs:
            if wv in text_lower:
                needs_rewrite = True
                reason = f"Starts with passive phrasing ('{wv}')."
                break
                
        if not needs_rewrite and not b.get("has_metrics") and b.get("word_count", 0) > 6:
            needs_rewrite = True
            reason = "Lacks measurable impact/metrics."

        if needs_rewrite:
            # Generate smart rewrite suggestion using STAR template
            # Extract key nouns/topics
            words = [w for w in text.split() if len(w) > 4 and w.lower() not in ["worked", "responsible", "helped", "assisted", "system", "using"]]
            key_subject = words[0] if words else "feature"
            
            rewritten = f"Architected and optimized {key_subject.lower()} capabilities, improving execution efficiency by 35% and enhancing system throughput across 50,000+ daily transactions."
            
            bullet_rewrites.append({
                "original": text,
                "issue": reason,
                "suggested": rewritten,
                "framework": "XYZ Formula: Accomplished [X], as measured by [Y], by doing [Z]"
            })
            if len(bullet_rewrites) >= 5:
                break

    # Determine Grade and Color Code
    if overall_score >= 85:
        grade = "Excellent (Top 10%)"
        rating_color = "emerald"
        verdict = "Your resume is highly optimized for ATS algorithms and recruiters. It clearly articulates technical competencies and quantifiable achievements."
    elif overall_score >= 70:
        grade = "Strong (Top 25%)"
        rating_color = "teal"
        verdict = "Your resume is competitive with a solid foundation. Addressing a few bullet point quantifications and keyword optimizations will elevate it to top-tier status."
    elif overall_score >= 50:
        grade = "Average / Needs Polish"
        rating_color = "amber"
        verdict = "Your resume has essential details but lacks strong impact metrics and keyword density, which may cause ATS filters to rank it lower."
    else:
        grade = "Needs Major Overhaul"
        rating_color = "rose"
        verdict = "Your resume is missing critical sections, quantifiable outcomes, and industry-standard keywords. Follow the recommended fixes below to pass ATS screening."

    return {
        "overall_score": overall_score,
        "grade": grade,
        "rating_color": rating_color,
        "verdict": verdict,
        "sub_scores": {
            "section_completeness": {"score": section_score, "label": "Section Completeness", "weight": "20%"},
            "impact_metrics": {"score": impact_score, "label": "Impact & Quantified Metrics", "weight": "25%"},
            "skill_depth": {"score": skills_score, "label": "Skill Breadth & Depth", "weight": "25%"},
            "formatting_brevity": {"score": length_score, "label": "Brevity & Formatting", "weight": "15%"},
            "keyword_density": {"score": keyword_score, "label": "ATS Keyword Optimization", "weight": "15%"}
        },
        "strengths": strengths,
        "improvements": improvements,
        "critical_issues": critical_issues,
        "bullet_rewrites": bullet_rewrites,
        "metrics_summary": {
            "total_words": word_count,
            "total_skills": total_skills,
            "quantified_bullets_count": quantified_count,
            "total_bullets_analyzed": len(bullets),
            "action_verbs_count": len(action_verbs)
        }
    }

