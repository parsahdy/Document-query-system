from langchain import LLMChain, PromptTempalte
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from django.conf import settings


api_token=settings.HUGGINGFACE_API_TOKEN

hf = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    huggingfacehub_api_token=api_token,
    model_kwargs={"temperature": 0.7, "max_new_tokens": 512}
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

embeddings = HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def build_vector_index(documents):
    all_chunks = []
    for doc in documents:
        chunks = text_splitter.split_text(doc.content)
        for chunk in chunks:
            all_chunks.append({
                "title": doc.title,
                "content": chunk
            })

    texts = [c["content"] for c in all_chunks]
    metadatas = [{"title": c["title"]} for c in all_chunks]

    vectorestore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return vectorestore


template = """
You are a helpful assistant.
Use ONLY the following relevant document chunks to answer the question.

Documents:
{documents}

Question: {question}

Give a concise and accurate answer based strictly on the provided document chunks.
"""

prompt = PromptTempalte(
    input_variables=["documents", "question"],
    template=template
)

chain = LLMChain(llm=hf, prompt=prompt)


def answer_with_document(question, documents, k=3):
    vectorstore = build_vector_index(documents)

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    relevant_chunks  = retriever.get_relevant_documents(question)

    docs_text = "\n\n".join(
        [f"-({chunk.metadata['title']}): {chunk.page_content}" for chunk in relevant_chunks ]
    )

    answer = chain.run({"documents": docs_text, "question": question})
    return answer, relevant_chunks 