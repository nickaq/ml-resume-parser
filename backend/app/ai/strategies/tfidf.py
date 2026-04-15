"""
TF-IDF based semantic similarity strategy with role-aware scoring.

Scoring (v2):
    vacancy_coverage  — skill overlap as % of vacancy requirements
    role_alignment    — domain match bonus (1.0 / 0.55 / 0.2)
    tfidf_cosine      — TF-IDF vocabulary similarity

    overall = 0.30 * coverage + 0.25 * role_alignment + 0.45 * tfidf
              × primary_skill_boost
"""

from app.ai.extraction import detect_skills
from app.ai.preprocessing import preprocess
from app.ai.profile_analyzer import (
    ResumeProfile,
    analyze_resume,
    compute_role_alignment,
    detect_vacancy_domain,
)
from app.ai.strategies.base import MatchScore, MatchingStrategy

W_COVERAGE = 0.30
W_ROLE = 0.25
W_TFIDF = 0.45


class TfidfStrategy(MatchingStrategy):
    """
    TF-IDF + cosine similarity matching.

    Uses scikit-learn's TfidfVectorizer to capture vocabulary overlap beyond
    exact keyword matches.  Combined with skill overlap for explainability.

    Requires: scikit-learn (pip install scikit-learn).
    """

    @property
    def name(self) -> str:
        return "tfidf"

    def match(
        self,
        resume_text: str,
        vacancies: list[dict],
        top_k: int = 20,
    ) -> list[MatchScore]:
        if not resume_text.strip():
            return []

        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        profile = analyze_resume(resume_text)
        resume_clean = preprocess(resume_text)

        # Build corpus: resume first, then all vacancies
        vacancy_texts: list[str] = []
        for v in vacancies:
            text = f"{v['title']} {v['description']}"
            if v.get("requirements"):
                text += f" {v['requirements']}"
            vacancy_texts.append(preprocess(text))

        corpus = [resume_clean] + vacancy_texts

        vectorizer = TfidfVectorizer(
            lowercase=False,
            max_features=10_000,
            sublinear_tf=True,
            ngram_range=(1, 2),
        )
        tfidf_matrix = vectorizer.fit_transform(corpus)

        resume_vec = tfidf_matrix[0:1]
        vacancy_vecs = tfidf_matrix[1:]
        similarities = cosine_similarity(resume_vec, vacancy_vecs).flatten()

        results: list[MatchScore] = []
        for idx, v in enumerate(vacancies):
            vacancy_text = f"{v['title']} {v['description']}"
            if v.get("requirements"):
                vacancy_text += f" {v['requirements']}"

            vacancy_skills = detect_skills(vacancy_text)
            vacancy_domain = detect_vacancy_domain(vacancy_text)

            matched = profile.all_skills & vacancy_skills
            missing = vacancy_skills - profile.all_skills

            coverage = len(matched) / len(vacancy_skills) if vacancy_skills else 0.0
            role_align = compute_role_alignment(profile.domain, vacancy_domain)
            tfidf_score = float(max(0.0, similarities[idx]))

            overall = W_COVERAGE * coverage + W_ROLE * role_align + W_TFIDF * tfidf_score

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
                    semantic_score=round(tfidf_score, 4),
                    matched_skills=sorted(matched),
                    missing_skills=sorted(missing),
                    explanation=_build_explanation(
                        profile, vacancy_domain, v["title"], v["company"],
                        matched, missing, vacancy_skills,
                        coverage, role_align, tfidf_score, overall,
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
    tfidf: float,
    overall: float,
) -> str:
    parts: list[str] = []

    # Match quality
    if overall >= 0.65:
        parts.append(f"Excellent match for your {profile.role_label} profile.")
    elif overall >= 0.45:
        parts.append(f"Good match — your {profile.role_label} background is relevant here.")
    elif overall >= 0.28:
        parts.append(f"Partial match with your {profile.role_label} profile.")
    else:
        parts.append(f"Limited overlap with your {profile.role_label} background.")

    # Role alignment
    if role_align >= 1.0:
        parts.append(f"This {title} role directly aligns with your primary domain.")
    elif role_align >= 0.5:
        parts.append("This role is adjacent to your primary focus — experience partially transfers.")
    else:
        parts.append(f"This position is outside your core {profile.domain} specialization.")

    # Text / vocabulary similarity
    sem_label = "strong" if tfidf >= 0.3 else "moderate" if tfidf >= 0.15 else "low"
    parts.append(f"Text similarity is {sem_label} ({tfidf:.0%}).")

    # Coverage
    if vacancy_skills:
        pct = int(coverage * 100)
        parts.append(f"You cover {pct}% of required skills ({len(matched)}/{len(vacancy_skills)}).")

    # Skills breakdown
    if matched:
        primary_matched = sorted(matched & profile.primary_skills)
        secondary_matched = sorted(matched - profile.primary_skills)
        if primary_matched:
            parts.append(f"Core strengths: {', '.join(primary_matched)}.")
        if secondary_matched:
            parts.append(f"Additional skills: {', '.join(secondary_matched)}.")

    # Missing
    if missing:
        top_missing = sorted(missing)[:4]
        if overall >= 0.45:
            parts.append(f"To strengthen your application, consider: {', '.join(top_missing)}.")
        else:
            parts.append(f"Key gaps: {', '.join(top_missing)}.")

    return " ".join(parts)
