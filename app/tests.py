import os
import sys
import django

from app.retriever import SimpleTFIDFRetriever
from app.models import Document, Query

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doc_qa.settings')  
django.setup()


def test_retriever():
    print("=== Testing SimpleTFIDFRetriever ===\n")

    doc1 = Document(title="Deep Learning", content="Deep learning is a subset of machine learning that uses neural networks with multiple layers.")
    doc2 = Document(title="Python Programming", content="Python is a high-level programming language used for web development and data science.")
    doc3 = Document(title="Machine Learning", content="Machine learning is a field of artificial intelligence that enables computers to learn from data.")

    test_docs = [doc1, doc2, doc3]
    retriever = SimpleTFIDFRetriever(docs=test_docs, min_similarity=0.0)

    print(f"Total documents loaded: {len(retriever.docs)}\n")

    print("Test 1: Query about neural networks")
    results = retriever.query("what is neural network?", top_k=2)
    print(f"Number of results: {len(results)}")
    for doc, score in results:
        print(f" - {doc.title}: {score:.4f}")
    print()

    print("Test 2: Query about 'Python programming'")
    results = retriever.query("Tell me about Python", top_k=2)
    print(f"Number of results: {len(results)}")
    for doc, score in results:
        print(f"  - {doc.title}: {score:.4f}")
    print()

    print("Test 3: Query about 'machine learning'")
    results = retriever.query("Explain machine learning", top_k=3)
    print(f"Number of results: {len(results)}")
    for doc, score in results:
        print(f"  - {doc.title}: {score:.4f}")
    print()

    print("Test 4: Unrelated query")
    results = retriever.query("What is cooking?", top_k=2)
    print(f"Number of results: {len(results)}")
    for doc, score in results:
        print(f"  - {doc.title}: {score:.4f}")
    print()
    
    print("=== Test completed ===")

if __name__ == "__main__":
    test_retriever()