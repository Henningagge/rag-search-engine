from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
import string

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        processed_title = preprocess_text(movie["title"])
        processed_querry = preprocess_text(query)
        if processed_querry in processed_title:
            results.append(movie)
            if len(results) >= limit:
                break
    return results


def preprocess_text(text: str) -> str:
    text = text.lower()
    chars = string.punctuation
    for char in chars:
        text = text.replace(char, "")
    return text