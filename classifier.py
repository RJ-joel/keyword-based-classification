CATEGORIES = {
    "Math": ["equation", "algebra", "geometry", "fraction", "integer", "variable",
        "calculus", "matrix", "theorem", "triangle", "square", "addition",
        "subtraction", "multiplication", "division", "percentage", "ratio"],
    
    "Science": ["plant", "photosynthesis", "atom", "force", "energy", "gravity",
        "physics", "chemistry", "biology", "matter", "molecule", "cell",
        "experiment", "ecosystem", "electricity", "motion"],
    
    "English": ["grammar", "noun", "verb", "pronoun", "sentence", "adjective",
        "adverb", "paragraph", "essay", "vocabulary", "reading", "writing",
        "literature", "poem", "story", "punctuation"],
}


def classify_text(text: str) -> str:
    text = text.lower()

    scores = {
        category: sum(text.count(keyword) for keyword in keywords)
        for category, keywords in CATEGORIES.items()
    }

    best_category = max(scores, key=scores.get)

    return best_category if scores[best_category] > 0 else "Unknown"