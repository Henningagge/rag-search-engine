from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
import string
from nltk.stem import PorterStemmer
import os.path
import pickle
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
    stemmer = PorterStemmer()
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

    for i in range(len(valid_tokens)):
        valid_tokens[i] = stemmer.stem(valid_tokens[i])
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


class InvertedIndex():
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        token_text = preprocess_text(text)
        for token in token_text:
            if token in self.index:
                token_ids = self.index[token]
                token_ids.add(doc_id)
                self.index[token] = token_ids
            else:
                self.index[token] = {doc_id}
    
    def get_document(self, term):
        lowerterm = term.lower()
        doc_ids = []
        if lowerterm in self.index:
            for id in self.index[lowerterm]:
                doc_ids.append(id)
        else:
            return []
        doc_sort =  sorted(doc_ids)
        return doc_sort

    def build(self):
        movies = load_movies()
        count = 0
        for m in movies:
            titel_descriptor = f"{m['title']} {m['description']}"
            self.__add_document(count, titel_descriptor)
            self.docmap[count] = m
            count += 1

    def save(self):
        path = "cache"
        path_index = "cache/index.pkl"
        path_doc = "cache/docmap.pkl"
        os.makedirs(path, exist_ok=True)

        with open(path_index, "wb") as file:
            pickle.dump(self.index, file)
        with open(path_doc, "wb") as file:
            pickle.dump(self.docmap, file)
        