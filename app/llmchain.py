from huggingface_hub import InferenceClient
from django.conf import settings

from .retriever import SimpleTFIDFRetriever

api_token = settings.HUGGINGFACE_API_TOKEN


client = InferenceClient(
    provider="novita",
    api_key=api_token,
)

def answer_with_document(question, top_k=3):
    retriever = SimpleTFIDFRetriever()
    results = retriever.query(question, top_k=top_k)

    if not results:
        return "No relevant documents found.", []

    docs_text = "\n\n".join([
        f"- ({doc.title}): {doc.content[:200]}... (Score: {score:.4f})"
        for doc, score in results
    ])

    prompt_text = f"""You are a helpful assistant.
    Use ONLY the following relevant document chunks to answer the question.

    Documents:
    {docs_text}

    Question: {question}

    Answer accurately using ONLY the documents."""

    
    messages = [{"role": "user", "content": prompt_text}]
    
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.2-1B-Instruct",
        messages=messages,
        max_tokens=512,
        temperature=0.3,
    )
    
    answer = completion.choices[0].message.content
    return answer, results
