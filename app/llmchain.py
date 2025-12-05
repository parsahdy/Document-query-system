from langchain import LLMChain, PromptTemplate
from langchain_community.llms import HuggingFaceHub
from django.conf import settings

from .retriever import SimpleTFIDFRetriever


api_token = settings.HUGGINGFACE_API_TOKEN

hf = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    huggingfacehub_api_token=api_token,
    model_kwargs={"temperature": 0.7, "max_new_tokens": 512}
)

template = """You are a helpful assistant.
Use ONLY the following relevant document chunks to answer the question.

Documents:
{documents}

Question: {question}

Give a concise and accurate answer based strictly on the provided document chunks.
"""

prompt = PromptTemplate(
    input_variables=["documents", "question"],
    template=template
)

chain = LLMChain(llm=hf, prompt=prompt)


def answer_with_document(question, top_k=3):
    retriever = SimpleTFIDFRetriever()
    results = retriever.query(question, top_k=top_k)

    if not results:
        return "No relevant documents found.", []
    
    docs_text = "\n\n".join([
        f"- ({doc.title}): {doc.content[:200]}... - Score: {score:.4f}"
        for doc, score in results
    ])

    answer = chain.run({
        "documents": docs_text,
        "question": question  
    })

    return answer, results