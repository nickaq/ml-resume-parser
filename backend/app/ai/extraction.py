"""
Skills extraction — detects known skills in preprocessed text.

Version 1 uses a controlled dictionary lookup (keyword matching).
This is intentionally simple and fast, and produces human-readable results.

EXTENSION POINTS:
  - Replace or augment this with TF-IDF vectorization.
  - Add a spaCy / transformer NER pipeline for context-aware extraction.
  - The interface (detect_skills → set[str]) is designed to stay stable.
"""

from app.ai.preprocessing import preprocess, tokenize
from app.ai.skills_db import SKILLS_DB


def detect_skills(text: str) -> set[str]:
    """
    Detect which known skills appear in the given text.

    Algorithm:
      1. Preprocess the text (lowercase, clean noise)
      2. Tokenize (stripping sentence-ending periods)
      3. For each alias in the skills dictionary, check if it appears
         as a contiguous token subsequence
      4. Return the set of canonical skill names found

    Args:
        text: Raw resume or vacancy text.

    Returns:
        A set of canonical skill names found in the text.
    """
    tokens = tokenize(preprocess(text))
    found: set[str] = set()

    for canonical_name, aliases in SKILLS_DB.items():
        for alias in aliases:
            if _alias_in_tokens(alias, tokens):
                found.add(canonical_name)
                break  # No need to check other aliases for this skill

    return found


def _alias_in_tokens(alias: str, tokens: list[str]) -> bool:
    """
    Check if an alias appears as a contiguous subsequence of tokens.

    This avoids false positives like matching "go" inside "ongoing"
    because we match at the token level.
    """
    alias_tokens = alias.split()
    n = len(alias_tokens)

    if n == 1:
        return alias_tokens[0] in tokens

    # Multi-word alias: check contiguous subsequence
    for i in range(len(tokens) - n + 1):
        if tokens[i : i + n] == alias_tokens:
            return True
    return False
