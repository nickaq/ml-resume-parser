"""AI / NLP module root — strategy-based recommendation engine."""

from app.ai.engine import RecommendationEngine  # noqa: F401
from app.ai.factory import get_strategy, list_strategies  # noqa: F401
from app.ai.strategies.base import MatchScore  # noqa: F401
