"""
Keyword-based matching strategy with role-aware scoring.

Scoring (v2):
    vacancy_coverage = |matched| / |vacancy_skills|   — how much of the job you cover
    role_alignment   = 1.0 / 0.55 / 0.2               — domain match bonus
    text_similarity  = token overlap                   — general vocabulary overlap

    overall = 0.45 * coverage + 0.30 * role_alignment + 0.25 * text_sim
              × primary_skill_boost (up to 1.2x)

The role alignment ensures that a Java Backend Developer scores much higher
on Java positions than on Frontend positions, even if a few React skills are listed.
"""

from app.ai.extraction import detect_skills
from app.ai.preprocessing import preprocess, tokenize
from app.ai.profile_analyzer import (
    ResumeProfile,
    analyze_resume,
    compute_role_alignment,
    detect_vacancy_domain,
)
from app.ai.strategies.base import MatchScore, MatchingStrategy

# ── Weights ────────────────────────────────────────────────────────
W_COVERAGE = 0.45
W_ROLE = 0.30
W_TEXT = 0.25


class KeywordStrategy(MatchingStrategy):
    """
    Fast keyword-based matching using a controlled skills dictionary.

    Best for: quick baselines, explainable results, low-resource environments.
    """

    @property
    def name(self) -> str:
        return "keyword"

    def match(
        self,
        resume_text: str,
        vacancies: list[dict],
        top_k: int = 20,
    ) -> list[MatchScore]:
        if not resume_text.strip():
            return []

        profile = analyze_resume(resume_text)
        resume_tokens = set(tokenize(preprocess(resume_text)))

        results: list[MatchScore] = []
        for v in vacancies:
            vacancy_text = f"{v['title']} {v['description']}"
            if v.get("requirements"):
                vacancy_text += f" {v['requirements']}"

            vacancy_skills = detect_skills(vacancy_text)
            vacancy_tokens = set(tokenize(preprocess(vacancy_text)))
            vacancy_domain = detect_vacancy_domain(vacancy_text)

            matched = profile.all_skills & vacancy_skills
            missing = vacancy_skills - profile.all_skills

            # Vacancy coverage: what % of required skills do I have?
            coverage = len(matched) / len(vacancy_skills) if vacancy_skills else 0.0

            # Role alignment
            role_align = compute_role_alignment(profile.domain, vacancy_domain)

            # Text similarity
            text_score = (
                len(resume_tokens & vacancy_tokens) / len(resume_tokens)
                if resume_tokens
                else 0.0
            )

            # Combined base score
            overall = W_COVERAGE * coverage + W_ROLE * role_align + W_TEXT * text_score

            # Primary skill boost: if most matched skills are from core domain
            if matched:
                primary_ratio = len(matched & profile.primary_skills) / len(matched)
                if primary_ratio > 0.4:
                    overall *= 1.0 + 0.2 * primary_ratio

            overall = round(min(max(overall, 0.0), 1.0), 4)

            results.append(
                MatchScore(
                    vacancy_id=v["id"],
                    title=v["title"],
                    company=v["company"],
                    overall_score=overall,
                    keyword_score=round(coverage, 4),
                    semantic_score=round(text_score, 4),
                    matched_skills=sorted(matched),
                    missing_skills=sorted(missing),
                    explanation=_build_explanation(
                        profile, vacancy_domain, v["title"], v["company"],
                        matched, missing, vacancy_skills, coverage, role_align, overall,
                    ),
                )
            )

        results.sort(key=lambda r: (-r.overall_score, r.title))
        return results[:top_k]


def _build_explanation(
    profile: ResumeProfile,
    vacancy_domain: str,
    title: str,
    company: str,
    matched: set[str],
    missing: set[str],
    vacancy_skills: set[str],
    coverage: float,
    role_align: float,
    overall: float,
) -> str:
    """Build a rich, contextual explanation of why this vacancy was matched."""
    parts: list[str] = []

    # 1. Match quality headline
    if overall >= 0.65:
        parts.append(f"Excellent match for your {profile.role_label} profile.")
    elif overall >= 0.45:
        parts.append(f"Good match — your {profile.role_label} background is relevant here.")
    elif overall >= 0.28:
        parts.append(f"Partial match with your {profile.role_label} profile.")
    else:
        parts.append(f"Limited overlap with your {profile.role_label} background.")

    # 2. Role alignment context
    if role_align >= 1.0:
        parts.append(
            f"This {title} position directly aligns with your primary domain."
        )
    elif role_align >= 0.5:
        parts.append(
            f"This role is adjacent to your primary focus, "
            f"so your experience partially transfers."
        )
    else:
        parts.append(
            f"This position is outside your core {profile.domain} specialization."
        )

    # 3. Skill coverage
    if vacancy_skills:
        pct = int(coverage * 100)
        parts.append(f"You cover {pct}% of the required skills ({len(matched)}/{len(vacancy_skills)}).")

    # 4. Matched skills — highlight primary vs secondary
    if matched:
        primary_matched = sorted(matched & profile.primary_skills)
        secondary_matched = sorted(matched - profile.primary_skills)
        if primary_matched:
            parts.append(f"Core strengths: {', '.join(primary_matched)}.")
        if secondary_matched:
            parts.append(f"Additional relevant skills: {', '.join(secondary_matched)}.")

    # 5. Missing skills with advice
    if missing:
        top_missing = sorted(missing)[:4]
        if overall >= 0.45:
            parts.append(
                f"To strengthen your application, consider adding: {', '.join(top_missing)}."
            )
        else:
            parts.append(f"Key gaps: {', '.join(top_missing)}.")

    return " ".join(parts)
