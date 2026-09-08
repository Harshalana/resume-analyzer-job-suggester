"""
CareerCraft AI - Generative Career Toolkit
Generates tailored cover letters, interview prep questions & STAR frameworks.
"""

from typing import Dict, Any, List


def generate_tailored_cover_letter(
    candidate_name: str,
    contact_info: Dict[str, Any],
    skills: List[str],
    experience_summary: str,
    job_title: str,
    company_name: str = "Hiring Team"
) -> str:
    """Generate a highly structured, professional, and tailored cover letter."""
    name = candidate_name if candidate_name and candidate_name != "Candidate" else "[Your Name]"
    email = contact_info.get("email") or "[your.email@example.com]"
    phone = contact_info.get("phone") or "[Your Phone Number]"
    linkedin = contact_info.get("linkedin") or ""
    
    top_skills = ", ".join(skills[:5]) if skills else "modern software engineering, system design, and collaborative development"
    
    company = company_name if company_name else "your organization"
    title = job_title if job_title else "the open position"

    cover_letter = f"""{name}
{email} | {phone}{f' | {linkedin}' if linkedin else ''}

[Date]

Hiring Manager / Talent Acquisition Team
{company}

Subject: Application for {title}

Dear Hiring Team,

I am writing to express my strong enthusiasm for the {title} position at {company}. With a proven track record in architecting high-performance solutions and proficiency in {top_skills}, I am excited about the opportunity to contribute directly to your team's mission and engineering excellence.

Throughout my career, I have focused on delivering scalable, maintainable, and high-impact technology solutions. For example, I have specialized in building robust architectures, automating mission-critical workflows, and collaborating cross-functionally to transform complex requirements into seamless user experiences. My technical toolkit across {top_skills} enables me to quickly ramp up, solve challenging system bottlenecks, and drive measurable outcomes.

What particularly draws me to {company} is your commitment to technical innovation and high standards of product execution. I thrive in collaborative environments where engineering rigour meets agile delivery, and I am eager to bring my problem-solving mindset and dedication to continuous improvement to your engineering initiatives.

Thank you for considering my application. I would welcome the opportunity to discuss how my background, technical expertise, and passion for engineering align with the goals of {company}.

Sincerely,

{name}
"""
    return cover_letter.strip()


def generate_interview_prep(
    candidate_skills: List[str],
    job_title: str,
    missing_skills: List[str]
) -> List[Dict[str, str]]:
    """Generate curated behavioral & technical interview questions with STAR answer guidelines."""
    questions = []
    
    # Question 1: Core Technical Architecture
    primary_skill = candidate_skills[0] if candidate_skills else "System Design"
    questions.append({
        "category": "Technical Deep Dive",
        "question": f"Can you walk us through a challenging project where you leveraged {primary_skill} to solve a critical bottleneck or scalability challenge?",
        "tip": "Focus on architectural trade-offs, how you evaluated alternatives, and the measurable impact (e.g. latency, throughput).",
        "star_framework": "• Situation: Describe the system constraint.\n• Task: Your responsibility.\n• Action: Specific technical decisions and implementation with " + primary_skill + ".\n• Result: Quantified improvement (e.g. 40% speedup, 99.9% uptime)."
    })

    # Question 2: Handling Skill Gaps / Upskilling
    if missing_skills:
        gap_skill = missing_skills[0]
        questions.append({
            "category": "Adaptability & Growth",
            "question": f"This role frequently utilizes {gap_skill}. How would you approach quickly mastering this technology and integrating it into our stack?",
            "tip": f"Demonstrate your proven ability to learn quickly by citing a past instance where you learned a new tool on the fly.",
            "star_framework": f"• Situation: Needed to deliver a feature using an unfamiliar tech stack.\n• Task: Rapidly onboard and maintain production-quality standards.\n• Action: Used documentation, built POCs, and sought targeted code reviews.\n• Result: Successfully delivered within deadline with zero regressions."
        })

    # Question 3: System Design & Resilience
    questions.append({
        "category": "System Design & Resilience",
        "question": f"How do you ensure high availability, monitoring, and error resilience when deploying services for a {job_title} role?",
        "tip": "Discuss health checks, graceful degradation, circuit breakers, structured logging, and automated CI/CD safeguards.",
        "star_framework": "• Situation: Critical service experiencing transient failures or scaling issues.\n• Task: Architect a resilient error-handling and observability pipeline.\n• Action: Integrated automated monitoring, retry strategies, and alert thresholds.\n• Result: Reduced mean time to recovery (MTTR) by 60%."
    })

    # Question 4: Behavioral & Collaboration
    questions.append({
        "category": "Behavioral / Leadership",
        "question": "Tell me about a time you had a technical disagreement with a colleague or product manager. How did you resolve it?",
        "tip": "Emphasize data-driven decision making, empathy, active listening, and alignment with business goals.",
        "star_framework": "• Situation: Differing perspectives on architecture vs timeline.\n• Task: Reach alignment without compromising code quality or release date.\n• Action: Benchmarked both approaches with a quick prototype and presented findings objectively.\n• Result: Reached consensus smoothly and delivered the feature on schedule."
    })

    # Question 5: Impact & Optimization
    questions.append({
        "category": "Measurable Impact",
        "question": "Describe an instance where you identified an inefficiency in an existing codebase or development workflow and took the initiative to fix it.",
        "tip": "Highlight proactiveness, developer experience (DevEx), and compounding team productivity gains.",
        "star_framework": "• Situation: Repetitive manual deployments or slow build cycles.\n• Task: Automate and modernize the developer workflow.\n• Action: Built automated CI/CD scripts and standardized linting/testing suites.\n• Result: Cut deployment time from 45 minutes to 6 minutes."
    })

    return questions

