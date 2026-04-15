"""
Matching engine v1 — computes a relevance score between a resume and a vacancy.

Scoring formula (v1):
  overall_score = 0.6 * skill_overlap_ratio + 0.4 * text_similarity_ratio

Where:
  - skill_overlap_ratio  = |resume_skills ∩ vacancy_skills| / |resume_skills ∪ vacancy_skills|
                            (Jaccard similarity of detected skill sets)
  - text_similarity_ratio = |resume_tokens ∩ vacancy_tokens| / |resume_tokens|
                            (What fraction of resume vocabulary appears in the vacancy)

If the resume has zero detected skills, we fall back to 100% text_similarity
so that results are still ranked meaningfully.

EXTENSION POINTS:
  - Replace skill_overlap_ratio with cosine similarity of TF-IDF vectors.
  - Replace text_similarity with sentence-transformer embedding cosine similarity.
  - Add weighting for skill rarity / seniority alignment.
  - The MatchResult dataclass is designed to stay stable across versions.
"""

from dataclasses import dataclass, field

from app.ai.extraction import detect_skills
from app.ai.preprocessing import preprocess


@dataclass
class MatchResult:
    """A scored vacancy match with human-readable explanation."""

    vacancy_id: int
    title: str
    company: str
    overall_score: float  # 0.0 – 1.0
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    short_explanation: str = ""


# ── Scoring weights ─────────────────────────────────────────────────
SKILL_WEIGHT = 0.6
TEXT_WEIGHT = 0.4


def match_resume_to_vacancy(
    resume_text: str,
    vacancy_title: str,
    vacancy_company: str,
    vacancy_description: str,
    vacancy_requirements: str | None = None,
    vacancy_id: int = 0,
) -> MatchResult:
    """
    Compute a match between one resume and one vacancy.

    Args:
        resume_text: Raw resume text.
        vacancy_title: Job title.
        vacancy_company: Company name.
        vacancy_description: Full vacancy description.
        vacancy_requirements: Optional requirements section.
        vacancy_id: The vacancy database ID.

    Returns:
        A MatchResult with score, matched/missing skills, and explanation.
    """
    # ── 1. Extract skills ───────────────────────────────────────────
    resume_skills = detect_skills(resume_text)

    # Combine description + requirements for vacancy text
    vacancy_text = f"{vacancy_title} {vacancy_description}"
    if vacancy_requirements:
        vacancy_text += f" {vacancy_requirements}"
    vacancy_skills = detect_skills(vacancy_text)

    # ── 2. Skill overlap (Jaccard) ──────────────────────────────────
    matched = resume_skills & vacancy_skills
    union = resume_skills | vacancy_skills
    # Skills that the vacancy needs but the resume doesn't have
    missing = vacancy_skills - resume_skills

    if union:
        skill_score = len(matched) / len(union)
    else:
        # No skills detected on either side — score from text only
        skill_score = 0.0

    # ── 3. Text similarity (vocabulary overlap) ─────────────────────
    resume_tokens = set(preprocess(resume_text).split())
    vacancy_tokens = set(preprocess(vacancy_text).split())

    if resume_tokens:
        text_score = len(resume_tokens & vacancy_tokens) / len(resume_tokens)
    else:
        text_score = 0.0

    # ── 4. Combined score ───────────────────────────────────────────
    if resume_skills:
        overall = SKILL_WEIGHT * skill_score + TEXT_WEIGHT * text_score
    else:
        # If no skills detected, rely entirely on text similarity
        overall = text_score

    overall = round(min(max(overall, 0.0), 1.0), 3)  # Clamp to [0, 1]

    # ── 5. Human-readable explanation ───────────────────────────────
    explanation = _build_explanation(overall, matched, missing, vacancy_title)

    return MatchResult(
        vacancy_id=vacancy_id,
        title=vacancy_title,
        company=vacancy_company,
        overall_score=overall,
        matched_skills=sorted(matched),
        missing_skills=sorted(missing),
        short_explanation=explanation,
    )


def _build_explanation(
    score: float,
    matched: set[str],
    missing: set[str],
    title: str,
) -> str:
    """Generate a short, human-readable explanation for the match."""
    if not matched and not missing:
        return f"Not enough skill data to assess fit for {title}."

    if not matched:
        top_missing = sorted(missing)[:3]
        return (
            f"The vacancy '{title}' looks for {', '.join(top_missing)} "
            f"which were not found in your resume."
        )

    top_matched = sorted(matched)[:3]
    parts = [f"Your resume shares {len(matched)} skill(s) with this role:"]
    parts.append(", ".join(top_matched))

    if missing:
        top_missing = sorted(missing)[:2]
        parts.append(f"Missing: {', '.join(top_missing)}")

    return " ".join(parts)
