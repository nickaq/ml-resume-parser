"""
Keyword-based matching strategy with role-aware and experience-aware scoring.

Scoring (v3):
    vacancy_coverage = |matched| / |vacancy_skills|   — how much of the job you cover
    role_alignment   = 1.0 / 0.55 / 0.2               — domain match bonus
    text_similarity  = token overlap                  — general vocabulary overlap

    overall = 0.45 * coverage + 0.30 * role_alignment + 0.25 * text_sim
    overall *= primary_skill_boost (up to +20%)
    overall *= title_match_boost (+30% if a primary skill is in title)
    overall *= experience_match_boost (penalizes if underqualified, boosts if matching)

This explicit scoring allows a Java dev with mid experience to be matched exactly
with Mid-level Java Vacancies.
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

            required_skills_set = set(v.get("required_skills", []) or [])
            nice_to_have_skills_set = set(v.get("nice_to_have_skills", []) or [])
            
            if required_skills_set or nice_to_have_skills_set:
                vacancy_skills = required_skills_set | nice_to_have_skills_set
            else:
                vacancy_skills = detect_skills(vacancy_text)

            vacancy_tokens = set(tokenize(preprocess(vacancy_text)))
            # Prioritize explicit domain if provided
            vacancy_domain = v.get("industry_domain") or detect_vacancy_domain(vacancy_text)
            vacancy_exp = v.get("experience_level", "mid") or "mid"

            matched = profile.all_skills & vacancy_skills
            missing = vacancy_skills - profile.all_skills
            
            strict_missing = required_skills_set - profile.all_skills

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

            # --- Strict Penalty for missing explicitly required skills ---
            if required_skills_set:
                if strict_missing:
                    # Drop score dramatically per missing required skill
                    penalty_factor = 0.5 ** len(strict_missing)
                    overall *= penalty_factor
                
            # --- Bonus for nice to have skills ---
            if nice_to_have_skills_set:
                nice_matched = profile.all_skills & nice_to_have_skills_set
                overall *= 1.0 + (0.1 * len(nice_matched))

            # --- Title Match Boost ---
            title_lower = preprocess(v['title'])
            title_matched_skill = None
            for skill in profile.primary_skills:
                if preprocess(skill) in title_lower:
                    title_matched_skill = skill
                    break
            
            if title_matched_skill:
                overall *= 1.30

            # --- Experience Match Boost/Penalty ---
            exp_match = False
            if profile.experience_level == vacancy_exp:
                overall *= 1.15
                exp_match = True
            elif profile.experience_level == "senior" and vacancy_exp == "mid":
                overall *= 1.05
            elif profile.experience_level == "mid" and vacancy_exp == "junior":
                overall *= 1.05
            elif profile.experience_level == "junior" and vacancy_exp == "senior":
                overall *= 0.50
            elif (profile.experience_level == "mid" and vacancy_exp == "senior") or \
                 (profile.experience_level == "junior" and vacancy_exp == "mid"):
                overall *= 0.80

            # Primary skill boost
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
                        vacancy_exp, exp_match, title_matched_skill, strict_missing
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
    vacancy_exp: str,
    exp_match: bool,
    title_matched_skill: str | None,
    strict_missing: set[str],
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

    # 2. Title and Role alignment context
    if title_matched_skill:
        parts.append(f"Your primary skill '{title_matched_skill}' directly matches the job title!")
    elif role_align >= 1.0:
        parts.append(f"This position directly aligns with your primary domain.")
    elif role_align >= 0.5:
        parts.append(f"This role is adjacent to your primary focus, so your experience partially transfers.")
    else:
        parts.append(f"This position is outside your core {profile.domain} specialization.")

    # 3. Experience Alignment
    if exp_match:
        parts.append(f"Your expected experience level exactly matches the required '{vacancy_exp}' level.")
    else:
        parts.append(f"The role prefers '{vacancy_exp}' experience, while your profile shows '{profile.experience_level}'.")

    # 4. Skill coverage
    if vacancy_skills:
        pct = int(coverage * 100)
        parts.append(f"You cover {pct}% of the required skills ({len(matched)}/{len(vacancy_skills)}).")

    # 5. Matched skills — highlight primary vs secondary
    if matched:
        primary_matched = sorted(matched & profile.primary_skills)
        secondary_matched = sorted(matched - profile.primary_skills)
        if primary_matched:
            parts.append(f"Core strengths: {', '.join(primary_matched)}.")
        if secondary_matched:
            parts.append(f"Additional relevant skills: {', '.join(secondary_matched)}.")

    # 6. Missing skills with advice
    if strict_missing:
        parts.append(f"Critical Gaps (Must Have): {', '.join(sorted(strict_missing))}. This heavily reduced your score.")
    elif missing:
        top_missing = sorted(missing)[:4]
        if overall >= 0.45:
            parts.append(f"To strengthen your application, consider highlighting: {', '.join(top_missing)}.")
        else:
            parts.append(f"Key gaps: {', '.join(top_missing)}.")

    return " ".join(parts)
