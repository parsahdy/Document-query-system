from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from django.conf import settings

from .retriever import SimpleTFIDFRetriever

api_token = settings.HUGGINGFACE_API_TOKEN

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-small",
    huggingfacehub_api_token=api_token,
    task="text2text-generation",
    max_new_tokens=512,
    temperature=0.3,
)

template = """
You are a helpful assistant.
Use ONLY the following relevant document chunks to answer the question.

Documents:
{documents}

Question: {question}

Answer accurately using ONLY the documents.
"""

prompt = PromptTemplate(
    input_variables=["documents", "question"],
    template=template
)

chain = prompt | llm


def answer_with_document(question, top_k=3):
    retriever = SimpleTFIDFRetriever()
    results = retriever.query(question, top_k=top_k)

    if not results:
        return "No relevant documents found.", []

    for idx, (doc, score) in enumerate(results):
        print(f"[Retriever] doc={doc.title}, score={score}")

    docs_text = "\n\n".join([
        f"- ({doc.title}): {doc.content[:200]}... (Score: {score:.4f})"
        for doc, score in results
    ])

    try:
        answer = chain.invoke({
            "documents": docs_text,
            "question": question,
        })
    except StopIteration:
        return "LLM returned nothing (StopIteration).", results

    return answer, results