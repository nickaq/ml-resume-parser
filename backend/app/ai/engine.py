"""
AI Recommendation Engine v2.

Orchestrates matching using a pluggable strategy pattern.
The strategy (keyword / tfidf / embeddings) is selected at runtime.

Usage:
    engine = RecommendationEngine()
    results = engine.generate(resume_text, vacancies, strategy="tfidf")
"""

from app.ai.factory import get_strategy, list_strategies
from app.ai.strategies.base import MatchScore


class RecommendationEngine:
    """
    Top-level entry point for the recommendation pipeline.

    Delegates the actual matching to a strategy implementation.
    This keeps the service layer stable — only the strategy parameter changes.
    """

    def generate(
        self,
        resume_text: str,
        vacancies: list[dict],
        top_k: int = 20,
        strategy: str = "keyword",
    ) -> list[MatchScore]:
        """
        Match a resume against vacancies using the specified strategy.

        Args:
            resume_text: Raw extracted text from the user's resume.
            vacancies:   List of dicts with at least {id, title, company, description}.
            top_k:       Maximum number of results.
            strategy:    One of 'keyword', 'tfidf', 'embeddings'.

        Returns:
            List of MatchScore sorted by overall_score descending.
        """
        matching = get_strategy(strategy)
        return matching.match(resume_text, vacancies, top_k=top_k)

    @staticmethod
    def available_strategies() -> list[dict[str, str]]:
        """Return metadata about all available strategies."""
        return list_strategies()
