"""
Resume profile analyzer — detects the candidate's primary role, domain,
and skill hierarchy from resume text.

This enables role-aware matching: a Java Backend Developer's resume
should strongly prefer Java backend vacancies over frontend positions,
even if the resume mentions some frontend skills.
"""

import re
from dataclasses import dataclass, field

from app.ai.extraction import detect_skills
from app.ai.preprocessing import preprocess


# ── Domain definitions ──────────────────────────────────────────────
DOMAIN_PROFILES: dict[str, dict] = {
    "backend": {
        "core_skills": {
            "Java", "Python", "Go", "Rust", "C#", "PHP", "Ruby", "Kotlin", "Scala",
            "FastAPI", "Django", "Flask", "Spring Boot", "Express", "Node.js",
            "Rails", "Laravel", "REST API", "GraphQL", "Microservices",
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Oracle", "SQL Server",
            "RabbitMQ", "Kafka", "gRPC", "Hibernate",
        },
        "keywords": [
            "backend", "back-end", "back end", "server-side", "server side",
            "api developer", "api engineer", "backend developer", "backend engineer",
            "java developer", "python developer", "go developer", "php developer",
            "ruby developer", "node developer", ".net developer", "c# developer",
            "spring boot", "microservices", "rest api",
        ],
        "label": "Backend Developer",
    },
    "frontend": {
        "core_skills": {
            "React", "Vue.js", "Angular", "Next.js", "Svelte",
            "JavaScript", "TypeScript",
            "Storybook", "Cypress",
        },
        "keywords": [
            "frontend", "front-end", "front end", "ui developer", "ui engineer",
            "frontend developer", "frontend engineer", "react developer",
            "vue developer", "angular developer", "web developer",
            "user interface",
        ],
        "label": "Frontend Developer",
    },
    "fullstack": {
        "core_skills": set(),  # detected by having both backend + frontend skills
        "keywords": [
            "fullstack", "full-stack", "full stack",
            "fullstack developer", "fullstack engineer",
        ],
        "label": "Fullstack Developer",
    },
    "data": {
        "core_skills": {
            "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
            "scikit-learn", "Pandas", "NumPy", "Data Analysis", "Data Visualization",
            "Matplotlib", "Jupyter", "R", "Spark", "Airflow",
        },
        "keywords": [
            "data scientist", "data analyst", "data engineer", "ml engineer",
            "machine learning engineer", "deep learning", "data science",
            "analytics", "ai engineer", "research scientist", "nlp engineer",
        ],
        "label": "Data / ML Engineer",
    },
    "devops": {
        "core_skills": {
            "Docker", "Kubernetes", "Terraform", "AWS", "GCP", "Azure",
            "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI", "Ansible",
            "Linux", "Nginx", "Prometheus", "Grafana", "Helm", "ArgoCD",
        },
        "keywords": [
            "devops", "sre", "site reliability", "infrastructure",
            "platform engineer", "cloud engineer", "devops engineer",
            "systems administrator", "sysadmin",
        ],
        "label": "DevOps / SRE Engineer",
    },
    "mobile": {
        "core_skills": {
            "Swift", "Kotlin", "React Native", "Flutter",
        },
        "keywords": [
            "ios developer", "android developer", "mobile developer",
            "mobile engineer", "react native developer", "flutter developer",
            "swiftui", "jetpack compose",
        ],
        "label": "Mobile Developer",
    },
    "embedded": {
        "core_skills": {"C++"},
        "keywords": [
            "embedded", "firmware", "rtos", "arm", "autosar", "can bus",
            "embedded developer", "embedded engineer", "systems engineer",
            "hardware", "microcontroller",
        ],
        "label": "Embedded / Systems Engineer",
    },
    "security": {
        "core_skills": {"OAuth"},
        "keywords": [
            "security engineer", "security analyst", "penetration testing",
            "pentest", "cybersecurity", "information security", "infosec",
            "owasp", "vulnerability",
        ],
        "label": "Security Engineer",
    },
    "qa": {
        "core_skills": {"Testing", "pytest", "Jest", "Selenium", "Playwright", "Cypress"},
        "keywords": [
            "qa engineer", "test engineer", "quality assurance",
            "test automation", "sdet", "qa automation",
        ],
        "label": "QA Engineer",
    },
}

# Domains that are "adjacent" — partial credit for role alignment
ADJACENT_DOMAINS: set[tuple[str, str]] = {
    ("backend", "fullstack"),
    ("frontend", "fullstack"),
    ("backend", "devops"),
    ("data", "backend"),
    ("mobile", "frontend"),
    ("backend", "data"),
    ("devops", "backend"),
    ("frontend", "mobile"),
    ("fullstack", "backend"),
    ("fullstack", "frontend"),
    ("qa", "backend"),
    ("qa", "frontend"),
}


@dataclass
class ResumeProfile:
    """Analyzed resume profile with domain, role, and skill hierarchy."""
    domain: str
    domain_confidence: float
    role_label: str
    primary_skills: set[str] = field(default_factory=set)
    secondary_skills: set[str] = field(default_factory=set)
    all_skills: set[str] = field(default_factory=set)
    experience_level: str = "mid"


def analyze_resume(text: str) -> ResumeProfile:
    """
    Analyze resume text to detect primary role, domain, and skill hierarchy.

    Returns a ResumeProfile with:
      - domain: the candidate's primary area (backend, frontend, data, etc.)
      - primary_skills: skills from the core domain (weighted high in scoring)
      - secondary_skills: other skills (weighted lower)
    """
    all_skills = detect_skills(text)
    text_lower = preprocess(text)

    # Score each domain
    domain_scores: dict[str, float] = {}
    for domain, profile in DOMAIN_PROFILES.items():
        if domain == "fullstack":
            continue

        core = profile["core_skills"]
        skill_overlap = len(all_skills & core)
        skill_score = skill_overlap / max(len(core), 1)

        keyword_hits = sum(1 for kw in profile["keywords"] if kw in text_lower)
        keyword_score = min(keyword_hits / max(len(profile["keywords"]) * 0.3, 1), 1.0)

        domain_scores[domain] = 0.55 * skill_score + 0.45 * keyword_score

    # Check for fullstack (has significant backend + frontend)
    be_score = domain_scores.get("backend", 0)
    fe_score = domain_scores.get("frontend", 0)
    if be_score > 0.08 and fe_score > 0.08:
        fs_keywords = DOMAIN_PROFILES["fullstack"]["keywords"]
        fs_bonus = sum(1 for kw in fs_keywords if kw in text_lower) * 0.12
        domain_scores["fullstack"] = min(be_score, fe_score) * 0.8 + fs_bonus

    # Pick winner
    if not domain_scores or max(domain_scores.values()) < 0.01:
        primary_domain = "backend"
        confidence = 0.0
    else:
        primary_domain = max(domain_scores, key=lambda k: domain_scores[k])
        confidence = domain_scores[primary_domain]

    # Split skills into primary (core domain) vs secondary
    if primary_domain == "fullstack":
        core = (
            DOMAIN_PROFILES["backend"]["core_skills"]
            | DOMAIN_PROFILES["frontend"]["core_skills"]
        )
    else:
        core = DOMAIN_PROFILES.get(primary_domain, {}).get("core_skills", set())

    primary_skills = all_skills & core
    secondary_skills = all_skills - primary_skills

    role_label = DOMAIN_PROFILES.get(primary_domain, {}).get("label", "Developer")
    exp_level = _detect_experience_level(text_lower)

    return ResumeProfile(
        domain=primary_domain,
        domain_confidence=round(min(confidence, 1.0), 3),
        role_label=role_label,
        primary_skills=primary_skills,
        secondary_skills=secondary_skills,
        all_skills=all_skills,
        experience_level=exp_level,
    )


def detect_vacancy_domain(vacancy_text: str) -> str:
    """Detect the primary domain of a vacancy from its title + description."""
    text_lower = preprocess(vacancy_text)
    vacancy_skills = detect_skills(vacancy_text)

    domain_scores: dict[str, float] = {}
    for domain, profile in DOMAIN_PROFILES.items():
        if domain == "fullstack":
            continue
        core = profile["core_skills"]
        skill_overlap = len(vacancy_skills & core)
        skill_score = skill_overlap / max(len(core), 1)

        keyword_hits = sum(1 for kw in profile["keywords"] if kw in text_lower)
        keyword_score = min(keyword_hits / max(len(profile["keywords"]) * 0.3, 1), 1.0)

        domain_scores[domain] = 0.55 * skill_score + 0.45 * keyword_score

    # Check for fullstack
    be = domain_scores.get("backend", 0)
    fe = domain_scores.get("frontend", 0)
    if be > 0.05 and fe > 0.05:
        fs_kws = DOMAIN_PROFILES["fullstack"]["keywords"]
        fs_bonus = sum(1 for kw in fs_kws if kw in text_lower) * 0.15
        domain_scores["fullstack"] = (be + fe) / 2 + fs_bonus

    if not domain_scores:
        return "backend"
    return max(domain_scores, key=lambda k: domain_scores[k])


def compute_role_alignment(resume_domain: str, vacancy_domain: str) -> float:
    """
    How well the resume's primary domain matches the vacancy's domain.
    Returns: 1.0 exact match, 0.55 adjacent, 0.2 unrelated.
    """
    if resume_domain == vacancy_domain:
        return 1.0
    if (resume_domain, vacancy_domain) in ADJACENT_DOMAINS:
        return 0.55
    return 0.2


def _detect_experience_level(text: str) -> str:
    """Heuristic experience level detection from resume text."""
    senior_kw = [
        "senior", "lead", "principal", "staff", "architect",
        "head of", "director", "cto", "vp of", "team lead",
    ]
    junior_kw = [
        "junior", "intern", "working student", "werkstudent",
        "trainee", "entry level", "entry-level", "graduate",
    ]

    for kw in senior_kw:
        if kw in text:
            return "senior"
    for kw in junior_kw:
        if kw in text:
            return "junior"

    years = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)', text
    )
    if years:
        mx = max(int(y) for y in years)
        if mx >= 5:
            return "senior"
        elif mx >= 2:
            return "mid"
        return "junior"

    return "mid"
