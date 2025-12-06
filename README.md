# Document Query System

A Django-based intelligent document retrieval and question-answering system that integrates:

* Custom TF‑IDF retriever
* LangChain-based LLM reasoning
* Semantic embeddings (FAISS + MiniLM)
* HuggingFaceHub LLM (Mistral-7B-Instruct-v0.2)

This project lets users upload documents, retrieve the most relevant text chunks, and generate LLM-powered answers stored inside the database.

---

## 1. System Architecture

### **Backend:** Django + PostgreSQL/MySQL/SQLite

* `Document` model: stores uploaded documents (title, content)
* `Query` model: stores user questions and generated LLM answers

### **Retrieval Layer**

1. **SimpleTFIDFRetriever**

   * Computes TF‑IDF vectors for all documents
   * Returns top‑k most similar documents based on cosine similarity

2. **Vector Store with LangChain**

   * Uses `RecursiveCharacterTextSplitter` to create chunks
   * Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
   * Index stored in **FAISS**
   * Supports semantic retrieval of the most relevant chunks

### **LLM Layer**

* Powered by **HuggingFaceHub**
* Model: `mistralai/Mistral-7B-Instruct-v0.2`
* Used through LangChain runtime (`prompt | model` pipeline)

---

## 2. Project Setup & Installation

### **Clone the repository:**

```
git clone https://github.com/<your-username>/Document-query-system.git
cd Document-query-system
```

### **Create virtual environment:**

```
python -m venv venv
source venv/bin/activate  (Linux/Mac)
venv\Scripts\activate   (Windows)
```

### **Install dependencies:**

```
pip install -r requirements.txt
```

### **Add HuggingFace Token:**

Inside `.env` or Django settings:

```
HUGGINGFACE_API_TOKEN="your_token_here"
```

### **Run migrations:**

```
python manage.py migrate
```

### **Start server:**

```
python manage.py runserver
```

---

## 3. How the LangChain Integration Works

### **Step 1: Build Vector Index**

Documents are split into chunks:

```
chunks = text_splitter.split_text(doc.content)
```

Then embeddings are generated and stored in FAISS:

```
vectorestore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
```

### **Step 2: Retrieve Relevant Chunks**

```
retriever = vectorestore.as_retriever(search_kwargs={"k": 3})
relevant_chunks = retriever.get_relevant_documents(question)
```

### **Step 3: LLM Answer Generation**

Uses the new LangChain pipeline API:

```
chain = prompt | llm
answer = chain.invoke({"documents": docs_text, "question": question})
```

The final answer is then stored in the `Query` model.

---

## 4. How to Use the System

### **1. Upload Documents**

Upload via Django admin panel or a custom upload endpoint.

### **2. Ask a Question**

Send a question to the corresponding API endpoint. Workflow:

1. SimpleTFIDFRetriever returns the most similar documents
2. Semantic retriever extracts relevant chunks
3. LLM processes the chunks and generates the answer
4. Answer saved into the database

### **3. View Results**

Answers are visible in Django Admin under **Queries**.

---

## 5. API Overview

### **POST /api/ask/**

Input:

```json
{
  "question": "What is deep learning?"
}
```

Output:

```json
{
  "answer": "Deep learning is ...",
  "documents_used": ["doc1", "doc2"]
}
```

---

## 6. Future Improvements

* Add streaming responses
* Add multi-language embeddings
* Include caching for faster retrieval

---

## License

MIT
