from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
import string

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    for movie in movies:
        query_tokens = preprocess_text(query)
        title_tokens = preprocess_text(movie["title"])
        if has_matching_token(query_tokens, title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break
    return results


def has_matching_token(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False


def preprocess_text(text: str) -> str:
    text = text.lower()
    chars = string.punctuation
    for char in chars:
        text = text.replace(char, "")
    text = text.split(" ")
    valid_tokens = []
    for token in text:
        if token:
            valid_tokens.append(token)
    valid_tokens = filter_stopwords(valid_tokens)
    return valid_tokens

def filter_stopwords(textlist: list[str]) -> list[str]:
    path = "/home/heagge/rag-search-engine/data/stopwords.txt"
    file =  open(path)
    file = file.read()
    file_arr = file.splitlines()
    for word in textlist:
        for filword in file_arr:
            if filword == word:
                textlist.remove(word)
    return textlist
