"""
Text preprocessing — cleans raw resume / vacancy text for analysis.

This module is deliberately simple and stateless.  It can be extended later
with stemming, lemmatization, or stop-word removal when the pipeline matures.
"""

import re


def preprocess(text: str) -> str:
    """
    Normalize raw text so downstream keyword matching is robust.

    Steps:
      1. Lowercase
      2. Remove common punctuation: commas, semicolons, colons, exclamation,
         question marks, quotes, parentheses, brackets, braces, <>, @, $, %,
         ^, &, =, ~, `, backslash
         (We keep periods and + for skills like "c++", "node.js", ".NET")
      3. Replace bullet points, dashes, pipes, underscores, asterisks, hashes
         with spaces
      4. Collapse runs of whitespace into a single space
      5. Strip leading / trailing whitespace

    Args:
        text: Raw text from a resume or vacancy.

    Returns:
        Cleaned text ready for keyword scanning.
    """
    if not text:
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation but keep + / . for skills like "c++" and "node.js"
    text = re.sub(r'[;:!?"\'\[\](){}<>@$%^&=~`\\,]', ' ', text)

    # 3. Replace bullet points, dashes, pipes, underscores, asterisks, hashes
    text = re.sub(r'[\u2022\u00b7\u25cf\u25aa\u25b8\u25ba\u2605\u2606\u2714\u2718\u2192\u2190\u2191\u2193\-\u2013\u2014|_#*]+', ' ', text)

    # 4. Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    # 5. Strip
    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Split preprocessed text into tokens.
    Strips leading/trailing periods from each token so "postgresql." → "postgresql".
    This handles sentence-ending periods without breaking "node.js" or ".NET".
    """
    raw_tokens = text.split()
    tokens: list[str] = []
    for t in raw_tokens:
        # Strip leading and trailing periods (but keep internal ones like node.js)
        t = t.strip('.')
        if t:
            tokens.append(t)
    return tokens


def extract_ngrams(text: str, n: int = 1) -> set[str]:
    """
    Return a set of contiguous n-grams (word-level) from preprocessed text.
    Useful for matching multi-word skill aliases.
    """
    words = tokenize(text)
    if n > len(words):
        return set()
    return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}
