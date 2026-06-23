import re
from collections import Counter
from functools import lru_cache

from nltk.stem import PorterStemmer

CATEGORIES = {
    "Math": [
        "equation", "algebra", "geometry", "fraction", "integer", "variable",
        "calculus", "matrix", "theorem", "triangle", "addition",
        "subtraction", "multiplication", "division", "percentage", "ratio",
    ],
    "Science": [
        "plant", "photosynthesis", "atom", "force", "energy", "gravity",
        "physics", "chemistry", "biology", "matter", "molecule", "cell",
        "experiment", "ecosystem", "electricity", "motion",
    ],
    "English": [
        "grammar", "noun", "verb", "pronoun", "sentence", "adjective",
        "adverb", "paragraph", "essay", "vocabulary", "reading", "writing",
        "literature", "poem", "story", "punctuation",
    ],
}

TOKEN_PATTERN = re.compile(r"[A-Za-z]+")
STEMMER = PorterStemmer()

# Useful irregular forms that a general stemmer may not normalize as expected.
IRREGULAR_FORMS = {
    "matrices": "matrix",
}


@lru_cache(maxsize=None)
def normalize_word(word: str) -> str:
    word = word.lower()
    word = IRREGULAR_FORMS.get(word, word)
    return STEMMER.stem(word)


STEMMED_KEYWORDS = {
    category: frozenset(normalize_word(keyword) for keyword in keywords)
    for category, keywords in CATEGORIES.items()
}


def classify_text(text: str) -> str:
    """
    Classify text using stemmed keywords.

    Examples:
    - equation / equations
    - variable / variables
    - plant / plants

    are treated as matching words.
    """
    tokens = TOKEN_PATTERN.findall(text.lower())
    token_counts = Counter(normalize_word(token) for token in tokens)

    scores = {
        category: sum(
            token_counts[keyword]
            for keyword in keywords
        )
        for category, keywords in STEMMED_KEYWORDS.items()
    }

    highest_score = max(scores.values())

    if highest_score == 0:
        return "Unknown"

    winners = [
        category
        for category, score in scores.items()
        if score == highest_score
    ]

    # A tie is ambiguous, so it is intentionally classified as Unknown.
    return winners[0] if len(winners) == 1 else "Unknown"