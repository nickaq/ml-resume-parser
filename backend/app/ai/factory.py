"""
Strategy factory — creates and caches matching strategies.

Usage:
    from app.ai.factory import get_strategy

    strategy = get_strategy("keyword")      # fast, explainable
    strategy = get_strategy("tfidf")        # vocabulary overlap
    strategy = get_strategy("embeddings")   # semantic similarity

The factory returns a cached instance per strategy name so that
embedding models are not re-downloaded and TF-IDF state is preserved.

Available strategies:
    keyword    — Controlled dictionary-based skill matching (v1)
    tfidf      — TF-IDF + cosine similarity (requires scikit-learn)
    embeddings — Sentence-transformer embeddings (requires sentence-transformers)
"""

from app.ai.strategies.base import MatchingStrategy

# ── Available strategy names ──────────────────────────────────────
AVAILABLE_STRATEGIES: set[str] = {"keyword", "tfidf", "embeddings"}

# ── Strategy singleton cache ──────────────────────────────────────
_strategy_cache: dict[str, MatchingStrategy] = {}


def get_strategy(name: str) -> MatchingStrategy:
    """
    Get a matching strategy by name (cached singleton).

    Args:
        name: One of 'keyword', 'tfidf', 'embeddings'.

    Returns:
        A MatchingStrategy instance.

    Raises:
        ValueError: If the strategy name is unknown.
    """
    normalised = name.lower().strip()
    if normalised not in AVAILABLE_STRATEGIES:
        raise ValueError(
            f"Unknown strategy '{name}'. "
            f"Available: {', '.join(sorted(AVAILABLE_STRATEGIES))}"
        )

    if normalised not in _strategy_cache:
        _strategy_cache[normalised] = _create_strategy(normalised)
    return _strategy_cache[normalised]


def _create_strategy(name: str) -> MatchingStrategy:
    """Internal creator — called only once per strategy name."""
    if name == "keyword":
        from app.ai.strategies.keyword import KeywordStrategy
        return KeywordStrategy()
    elif name == "tfidf":
        from app.ai.strategies.tfidf import TfidfStrategy
        return TfidfStrategy()
    elif name == "embeddings":
        from app.ai.strategies.embeddings import EmbeddingStrategy
        return EmbeddingStrategy()
    raise ValueError(f"Unknown strategy: {name}")


def list_strategies() -> list[dict[str, str]]:
    """Return metadata about all available strategies (for UI / API docs)."""
    from app.ai.strategies.embeddings import EmbeddingStrategy
    from app.ai.strategies.keyword import KeywordStrategy
    from app.ai.strategies.tfidf import TfidfStrategy

    instances: list[MatchingStrategy] = [
        KeywordStrategy(),
        TfidfStrategy(),
        EmbeddingStrategy(),
    ]
    return [
        {"name": s.name, "description": s.description}
        for s in instances
    ]
