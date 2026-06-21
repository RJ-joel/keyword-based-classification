import re

CATEGORIES = {
    "Math": [
        "equation", "algebra", "geometry", "fraction", "integer", "variable",
        "calculus", "matrix", "theorem", "triangle", "addition",
        "subtraction", "multiplication", "division", "percentage", "ratio"
    ],
    "Science": [
        "plant", "photosynthesis", "atom", "force", "energy", "gravity",
        "physics", "chemistry", "biology", "matter", "molecule", "cell",
        "experiment", "ecosystem", "electricity", "motion"
    ],
    "English": [
        "grammar", "noun", "verb", "pronoun", "sentence", "adjective",
        "adverb", "paragraph", "essay", "vocabulary", "reading", "writing",
        "literature", "poem", "story", "punctuation"
    ],
}


def classify_text(text: str) -> str:
    text = text.lower()

    scores = {
        category: sum(
            len(re.findall(rf"\b{re.escape(keyword)}\b", text))
            for keyword in keywords
        )
        for category, keywords in CATEGORIES.items()
    }

    highest_score = max(scores.values())

    # Empty text or no keyword match
    if highest_score == 0:
        return "Unknown"

    winners = [
        category
        for category, score in scores.items()
        if score == highest_score
    ]

    # Example: Math = 3 and Science = 3
    if len(winners) > 1:
        return "Unknown"

    return winners[0]