"""
Strategy pattern base class for recommendation matching.

Each matching strategy (keyword, TF-IDF, embeddings) inherits from this
abstract base and implements the ``match`` method.  The factory in
``app/ai/factory.py`` selects the correct implementation at runtime.

This design keeps the rest of the application (routes, services) unchanged
when a new strategy is added.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class MatchScore:
    """
    Detailed score breakdown for a single resume–vacancy match.

    Fields:
        vacancy_id:     Database ID of the matched vacancy.
        title:          Vacancy title.
        company:        Company name.
        overall_score:  Final weighted score in [0, 1].
        keyword_score:  Skill-overlap / keyword-based component [0, 1].
        semantic_score: TF-IDF or embedding-based component [0, 1].
        matched_skills: Canonical skill names found in BOTH resume and vacancy.
        missing_skills: Skills found in vacancy but NOT in resume.
        explanation:    Human-readable summary of why this match was scored.
    """

    vacancy_id: int
    title: str
    company: str
    overall_score: float
    keyword_score: float = 0.0
    semantic_score: float = 0.0
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    explanation: str = ""

    def to_dict(self) -> dict:
        """Serialize to a plain dict (useful for JSON storage)."""
        return {
            "vacancy_id": self.vacancy_id,
            "title": self.title,
            "company": self.company,
            "overall_score": self.overall_score,
            "keyword_score": self.keyword_score,
            "semantic_score": self.semantic_score,
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "explanation": self.explanation,
        }


class MatchingStrategy(ABC):
    """
    Abstract base for all matching strategies.

    Subclasses must implement ``match`` which takes a resume text and a list
    of vacancy dicts, and returns a list of ``MatchScore`` objects sorted by
    ``overall_score`` descending.
    """

    @abstractmethod
    def match(
        self,
        resume_text: str,
        vacancies: list[dict],
        top_k: int = 20,
    ) -> list[MatchScore]:
        """
        Rank vacancies for a given resume.

        Args:
            resume_text: Raw or preprocessed resume text.
            vacancies:   Each dict needs at least {id, title, company, description}.
                         Optional: {requirements}.
            top_k:       Maximum number of results.

        Returns:
            Sorted list of MatchScore (highest first).
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Short identifier for this strategy (e.g. 'keyword', 'tfidf', 'embeddings')."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description shown in the API / UI."""
        return self.__doc__ or self.name
