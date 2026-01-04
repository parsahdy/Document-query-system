```markdown
# Document Query System

A Django-based intelligent document retrieval and question-answering system that combines custom TF-IDF retrieval, semantic embeddings (FAISS + MiniLM), and LLM reasoning powered by HuggingFace InferenceClient [web:20][web:22].

---

## Features

* Custom TF-IDF retriever for document similarity
* Semantic embeddings with FAISS vector store
* LLM-powered answers using Llama-3.2-1B-Instruct via HuggingFace InferenceClient
* PostgreSQL database for storing documents and queries
* Docker Compose for easy deployment

---

## Quick Start with Docker Compose

### Prerequisites

* Docker and Docker Compose installed
* HuggingFace API token ([get it here](https://huggingface.co/settings/tokens))

### Setup

**1. Clone the repository:**
```bash
git clone https://github.com/<your-username>/Document-query-system.git
cd Document-query-system
```

**2. Create `.env` file:**
```bash
HUGGINGFACE_API_TOKEN=your_token_here
POSTGRES_DB=docquery
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

**3. Start the application:**
```bash
docker-compose up -d --build
```

**4. Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

**5. Create superuser (optional):**
```bash
docker-compose exec web python manage.py createsuperuser
```

**6. Access the application:**
- Django app: http://localhost:8000
- Admin panel: http://localhost:8000/admin

**7. Stop the application:**
```bash
docker-compose down
```

---

## System Architecture

### Backend
Django with PostgreSQL stores documents (title, content) and queries (questions, LLM answers) [web:20][web:23].

### Retrieval Layer

**SimpleTFIDFRetriever**: Computes TF-IDF vectors and returns top-k documents by cosine similarity [web:13].

**Vector Store**: Uses `RecursiveCharacterTextSplitter` for chunking, `sentence-transformers/all-MiniLM-L6-v2` for embeddings, and FAISS for semantic search [web:13].

### LLM Layer

Powered by HuggingFace InferenceClient with `meta-llama/Llama-3.2-1B-Instruct` model through novita provider [web:13][web:26].

---

## How It Works

**1. Upload Documents**: Via Django admin or API endpoint

**2. Ask Questions**: The system retrieves relevant chunks using TF-IDF and semantic search

**3. Generate Answers**: LLM processes the chunks and generates contextual answers

**4. Store Results**: Answers saved in the database for future reference

---

## API Usage

### Ask a Question

**Endpoint:** `POST /api/ask/`

**Request:**
```json
{
  "question": "What is deep learning?"
}
```

**Response:**
```json
{
  "answer": "Deep learning is...",
  "documents_used": ["doc1", "doc2"]
}
```

---

## Project Structure

```
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── manage.py
└── app/
    ├── models.py
    ├── retriever.py
    └── views.py
```

---

## Future Improvements

* Add streaming responses for real-time answers
* Support multi-language embeddings
* Implement caching for faster retrieval
* Add document preprocessing pipeline

---

## License

MIT
