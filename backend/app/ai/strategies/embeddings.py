"""
Embedding-based semantic similarity strategy with role-aware scoring.

Scoring (v2):
    vacancy_coverage  — skill overlap as % of vacancy requirements
    role_alignment    — domain match bonus (1.0 / 0.55 / 0.2)
    embedding_cosine  — deep semantic similarity

    overall = 0.20 * coverage + 0.25 * role_alignment + 0.55 * embedding
              × primary_skill_boost

The embedding model captures deeper semantic meaning — "built REST APIs"
is close to "API development" even without shared tokens.  Combined with
role alignment, a Java developer's resume will be semantically closer to
Java backend roles than to unrelated frontend positions.

Model: all-MiniLM-L6-v2 (384 dims, fast, good quality).
"""

import threading

from app.ai.extraction import detect_skills
from app.ai.preprocessing import preprocess
from app.ai.profile_analyzer import (
    ResumeProfile,
    analyze_resume,
    compute_role_alignment,
    detect_vacancy_domain,
)
from app.ai.strategies.base import MatchScore, MatchingStrategy

DEFAULT_MODEL = "all-MiniLM-L6-v2"

_model_cache: dict[str, object] = {}
_model_lock = threading.Lock()

W_COVERAGE = 0.20
W_ROLE = 0.25
W_EMBED = 0.55


class EmbeddingStrategy(MatchingStrategy):
    """
    Embedding-based matching using sentence-transformers.

    Captures semantic similarity beyond exact keyword overlap.
    Requires: sentence-transformers (pip install sentence-transformers).

    The model is loaded lazily on first use and cached for subsequent calls.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name

    @property
    def name(self) -> str:
        return "embeddings"

    @property
    def description(self) -> str:
        return (
            f"Semantic matching using sentence-transformers ({self.model_name}). "
            "Captures meaning beyond keyword overlap."
        )

    def _get_model(self):
        if self.model_name in _model_cache:
            return _model_cache[self.model_name]

        with _model_lock:
            if self.model_name not in _model_cache:
                try:
                    from sentence_transformers import SentenceTransformer
                except ImportError:
                    raise ValueError(
                        "Embeddings strategy requires the 'sentence-transformers' package. "
                        "Install it with: pip install sentence-transformers. "
                        "Note: Python 3.14+ may not be supported yet — use 'keyword' or 'tfidf' strategy instead."
                    )
                _model_cache[self.model_name] = SentenceTransformer(self.model_name)
            return _model_cache[self.model_name]

    def match(
        self,
        resume_text: str,
        vacancies: list[dict],
        top_k: int = 20,
    ) -> list[MatchScore]:
        if not resume_text.strip():
            return []

        model = self._get_model()
        from sklearn.metrics.pairwise import cosine_similarity

        profile = analyze_resume(resume_text)
        resume_clean = preprocess(resume_text)

        vacancy_texts: list[str] = []
        for v in vacancies:
            text = f"{v['title']} {v['description']}"
            if v.get("requirements"):
                text += f" {v['requirements']}"
            vacancy_texts.append(preprocess(text))

        embeddings = model.encode([resume_clean] + vacancy_texts, convert_to_numpy=True)
        resume_emb = embeddings[0:1]
        vacancy_embs = embeddings[1:]
        similarities = cosine_similarity(resume_emb, vacancy_embs).flatten()

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
            emb_score = float(max(0.0, similarities[idx]))

            overall = W_COVERAGE * coverage + W_ROLE * role_align + W_EMBED * emb_score

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
                    semantic_score=round(emb_score, 4),
                    matched_skills=sorted(matched),
                    missing_skills=sorted(missing),
                    explanation=_build_explanation(
                        profile, vacancy_domain, v["title"], v["company"],
                        matched, missing, vacancy_skills,
                        coverage, role_align, emb_score, overall,
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
    emb_score: float,
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

    # Semantic fit
    sem_label = "strong" if emb_score >= 0.55 else "good" if emb_score >= 0.4 else "moderate" if emb_score >= 0.25 else "weak"
    parts.append(f"Semantic similarity is {sem_label} ({emb_score:.0%}).")

    # Coverage
    if vacancy_skills:
        pct = int(coverage * 100)
        parts.append(f"You cover {pct}% of required skills ({len(matched)}/{len(vacancy_skills)}).")

    # Skills
    if matched:
        primary_matched = sorted(matched & profile.primary_skills)
        secondary_matched = sorted(matched - profile.primary_skills)
        if primary_matched:
            parts.append(f"Core strengths: {', '.join(primary_matched)}.")
        if secondary_matched:
            parts.append(f"Additional skills: {', '.join(secondary_matched)}.")

    if missing:
        top_missing = sorted(missing)[:4]
        if overall >= 0.45:
            parts.append(f"To strengthen your application, consider: {', '.join(top_missing)}.")
        else:
            parts.append(f"Key gaps: {', '.join(top_missing)}.")

    return " ".join(parts)
