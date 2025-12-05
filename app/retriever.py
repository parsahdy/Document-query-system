from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from .models import Document


class SimpleTFIDFRetriever:
    def __init__(self, docs=None, min_similarity: float = 0.0):
        if docs is None:
            docs = Document.objects.all()

        self.docs = list(docs)
        self.min_similarity = min_similarity
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = self._build_index()

    def _build_index(self):
        if not self.docs:
            return None
        
        texts = [doc.content for doc in self.docs]
        return self.vectorizer.fit_transform(texts)
    
    def query(self, question: str, top_k: int = 3) -> List[Tuple]:
        if self.tfidf_matrix is None or not question.strip():
            return []
        
        query_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            similarity_score = similarities[idx]
            if similarity_score > self.min_similarity:
                results.append((self.docs[idx], similarity_score.item()))
        
        return results

    def add_documents(self, new_docs: List) -> None:
        self.docs.extend(new_docs)
        self.tfidf_matrix = self._build_index()