# Jango — Enterprise Document Intelligence Platform

> A private AI-powered document assistant that lets users upload enterprise documents, search their content semantically, and ask questions using Retrieval-Augmented Generation (RAG).

Jango is a full-stack AI knowledge assistant designed around a simple idea:

**Your documents → semantic retrieval → grounded AI answers.**

Instead of relying on the model's general knowledge, Jango retrieves relevant information from uploaded documents and uses that context to generate answers with document and page references.

---

## 🚀 Live Demo

### Frontend
https://enterprise-document-iipopko80-utkarsh-0106s-projects.vercel.app/register

> The frontend is deployed using Vercel.

### Backend

The FastAPI backend can be exposed securely for development/demo purposes using Cloudflare Tunnel.

> Note: The current demo backend runs from the developer's local environment through a Cloudflare Quick Tunnel. Quick Tunnel URLs are temporary and may change when the tunnel is restarted.

---

# ✨ Features

## 🔐 Authentication

- User registration
- User login
- JWT-based authentication
- Protected API endpoints
- Current-user authentication
- User-specific document access

## 📄 Document Management

- Upload PDF documents
- PDF validation
- File size validation
- Secure filename handling
- Document listing
- Document deletion
- Document processing status
- Background document ingestion

## 🧠 AI-Powered RAG

- Semantic document search
- Context-aware question answering
- Retrieval-Augmented Generation
- Source-aware responses
- Page-level document references
- Configurable number of retrieved chunks
- Answers grounded only in uploaded documents
- Prevents unsupported answers by returning:

> "I don't know based on the uploaded documents."

## 🗃️ Vector Search

- Chroma vector database
- Persistent local vector storage
- User-isolated document retrieval
- Metadata-aware document chunks
- Semantic similarity search

## 🤖 Local AI

Jango uses Ollama instead of paid proprietary AI APIs.

### Chat Model

- Qwen3 8B

### Embedding Model

- nomic-embed-text

This allows the AI pipeline to run locally without requiring an OpenAI API key.

## 🎨 Modern SaaS UI

- React-based interface
- Responsive dashboard
- Modern dark AI-focused design
- Jango AI branding
- Document management interface
- AI chat interface
- Source references
- Authentication screens
- Sidebar navigation

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────────┐
                    │        User Browser      │
                    │                          │
                    │      React + Vite        │
                    └────────────┬─────────────┘
                                 │
                                 │ HTTPS
                                 ▼
                    ┌──────────────────────────┐
                    │         Vercel           │
                    │                          │
                    │    React Frontend        │
                    └────────────┬─────────────┘
                                 │
                                 │ REST API
                                 ▼
                    ┌──────────────────────────┐
                    │        FastAPI           │
                    │                          │
                    │ Authentication           │
                    │ Document APIs             │
                    │ RAG API                   │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴─────────────┐
                    │                          │
                    ▼                          ▼
          ┌──────────────────┐       ┌──────────────────┐
          │     Chroma       │       │     SQLite       │
          │                  │       │                  │
          │ Vector Storage   │       │ User/Documents   │
          └────────┬─────────┘       └──────────────────┘
                   │
                   │ Semantic Retrieval
                   ▼
          ┌──────────────────┐
          │     Ollama       │
          │                  │
          │ nomic-embed-text │
          │ Qwen3 8B         │
          └──────────────────┘


🔄 RAG Pipeline

When a user asks a question, Jango follows this pipeline:
User Question
      │
      ▼
FastAPI RAG Endpoint
      │
      ▼
Generate Query Embedding
      │
      ▼
Chroma Similarity Search
      │
      ▼
Retrieve Relevant Document Chunks
      │
      ▼
Build Context
      │
      ▼
Send Context + Question to Qwen3
      │
      ▼
Generate Grounded Answer
      │
      ▼
Return Answer + Sources
      │
      ▼
React Chat Interface

📚 Document Ingestion Pipeline

When a PDF is uploaded:

PDF Upload
    │
    ▼
Validate File
    │
    ├── Check MIME type
    ├── Check file size
    ├── Check file content
    └── Check encrypted PDF
    │
    ▼
Store PDF
    │
    ▼
Extract Text
    │
    ▼
Split Document into Chunks
    │
    ▼
Generate Embeddings
    │
    ▼
Store Vectors in Chroma
    │
    ▼
Document Ready for AI Search

🛠️ Tech Stack
Frontend
React
Vite
JavaScript
Axios
CSS
Backend
Python
FastAPI
SQLAlchemy
Pydantic
JWT Authentication
Uvicorn
AI / RAG
Ollama
Qwen3 8B
nomic-embed-text
LangChain
LangChain Ollama
LangChain Chroma
Database & Storage
SQLite
Chroma
Local file storage
Deployment / Infrastructure
Vercel
Cloudflare Tunnel
GitHub

📁 Project Structure

enterprise-document-rag/
│
├── alembic/
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── auth.py
│   │   │
│   │   ├── routers/
│   │   │   ├── documents.py
│   │   │   └── rag.py
│   │   │
│   │   ├── services/
│   │   │   ├── rag.py
│   │   │   └── vector_store.py
│   │   │
│   │   ├── schemas/
│   │   │   └── ...
│   │   │
│   │   ├── models/
│   │   │   └── ...
│   │   │
│   │   ├── db.py
│   │   ├── main.py
│   │   └── settings.py
│   │
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js
│   │   │
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   └── AskJangoCard.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Chat.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│   └── ...
│
├── main.py
├── alembic.ini
├── pytest.ini
├── .gitignore
└── README.md

⚙️ Local Setup
1. Clone the repository
git clone https://github.com/utkarsh-0106/enterprise-document-rag.git
cd enterprise-document-rag
🐍 2. Create Python Virtual Environment
python3 -m venv backend/.venv

Activate it:

source backend/.venv/bin/activate
📦 3. Install Backend Dependencies
pip install -r backend/requirements.txt
🤖 4. Install Ollama

Install Ollama on your machine.

Then make sure Ollama is running.

Verify:

curl http://localhost:11434/api/tags
🧠 5. Pull AI Models

Pull the chat model:

ollama pull qwen3:8b

Pull the embedding model:

ollama pull nomic-embed-text

Verify:

ollama list

You should see:

qwen3:8b
nomic-embed-text
🔧 6. Environment Variables

Create:

backend/.env

Example:

DATABASE_URL=sqlite:///./sql_app.db

SECRET_KEY=replace-with-a-secure-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_EMBEDDING_MODEL=nomic-embed-text

OLLAMA_CHAT_MODEL=qwen3:8b

CHROMA_PERSIST_DIRECTORY=./storage/chroma

For production, use a strong randomly generated SECRET_KEY.

▶️ 7. Start the Backend

From the project root:

uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000
❤️ 8. Test Backend Health
curl http://127.0.0.1:8000/api/health

Expected response:

{
  "status": "healthy"
}
📖 9. API Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs

Available API areas include:

Authentication
    POST /api/auth/register
    POST /api/auth/login
    GET  /api/auth/me

Documents
    POST   /api/documents/upload
    GET    /api/documents/
    DELETE /api/documents/{document_id}
    GET    /api/documents/{document_id}/status

RAG
    POST /api/rag/query

Health
    GET /api/health
💻 Frontend Setup

Open another terminal.

cd frontend

Install dependencies:

npm install

Create:

frontend/.env

For local development:

VITE_API_URL=http://localhost:8000

Start the frontend:

npm run dev

The Vite development server will provide the frontend URL in the terminal.

🌐 Frontend Deployment

The React frontend is deployed using Vercel.

The frontend uses:

VITE_API_URL

to determine which backend API it communicates with.

For a deployed environment:

VITE_API_URL=<YOUR_PUBLIC_BACKEND_URL>

After changing the environment variable, redeploy the frontend.

☁️ Backend Exposure for Development

For development/demo purposes, the local FastAPI server can be exposed through Cloudflare Quick Tunnel.

Install Cloudflare Tunnel:

brew install cloudflared

Start FastAPI:

uvicorn main:app --reload

Then create a tunnel:

cloudflared tunnel --url http://127.0.0.1:8000

Cloudflare will provide a temporary HTTPS URL such as:

https://example.trycloudflare.com

Test it:

curl https://example.trycloudflare.com/api/health

Expected:

{
  "status": "healthy"
}

Use the generated HTTPS URL as the frontend's:

VITE_API_URL
🔐 Security

Jango implements several security measures:

JWT authentication
Protected API routes
User-specific document filtering
Password hashing
PDF validation
File size restrictions
Sanitized uploaded filenames
Encrypted PDF rejection
Environment-based secrets
CORS middleware
🧠 Why RAG?

Traditional LLM applications can generate answers from their pretrained knowledge.

That creates a problem for enterprise documents.

For example:

User:
"What is the company's leave policy?"

Traditional LLM:
May not know the company's internal policy.

Jango:
1. Searches uploaded company documents.
2. Retrieves relevant chunks.
3. Sends those chunks to Qwen3.
4. Generates an answer using the retrieved context.
5. Provides the source document and page.

This makes the system much more suitable for private organizational knowledge.

🎯 Design Goals

Jango was designed around the following principles:

Privacy

Documents should remain within the application's controlled infrastructure instead of automatically being sent to third-party AI APIs.

Grounded Answers

The AI should answer using retrieved document context instead of inventing information.

User Isolation

Users should only retrieve documents associated with their own account.

Modularity

Authentication, document processing, vector search, and RAG generation are separated into independent backend modules.

Extensibility

The architecture is designed so that additional:

AI models
vector databases
document types
authentication providers
cloud storage
enterprise integrations

can be added later.

📈 Future Improvements

Planned improvements include:

PostgreSQL production database
Persistent cloud object storage
Persistent cloud vector database
Background job queue
Redis caching
Streaming AI responses
More document formats
Document preview
Advanced metadata filtering
Team workspaces
Role-based access control
Admin dashboard
Conversation history
AI-generated document summaries
Hybrid keyword + vector search
Reranking models
Observability and monitoring
Production-grade cloud deployment
Scalable GPU inference infrastructure
🧪 Testing

The project includes a test suite under:

tests/

Run tests using:

pytest
📊 Engineering Highlights

This project demonstrates practical implementation of:

REST API development
FastAPI backend architecture
JWT authentication
SQLAlchemy database integration
PDF processing
Background processing
Vector databases
Semantic search
Embeddings
Retrieval-Augmented Generation
Local LLM inference
Prompt engineering
User-level data isolation
React frontend development
API integration
Environment configuration
Cloud deployment
Cloudflare tunneling
Git/GitHub workflow
👨‍💻 Author

Utkarsh Maheshwari

B.Tech Computer Science & Engineering

⭐ Project

If you find the architecture or implementation useful, consider giving the repository a star.

GitHub:

https://github.com/utkarsh-0106/enterprise-document-rag


### One important thing

I deliberately **didn't call it a fully production backend deployment** in the README. Your Vercel frontend is deployed, but your FastAPI + Ollama backend is currently being exposed from your Mac through a **Cloudflare Quick Tunnel**. That's perfectly fine for a portfolio/demo stage, and it's much better than falsely claiming you have a permanent cloud GPU backend.

Also, your README should **not contain your actual `SECRET_KEY`** or any private credentials.

For your resume, I would use this project description:

> **Jango — Enterprise Document Intelligence Platform | React, FastAPI, Ollama, LangChain, Chroma, SQLite**  
> • Built a full-stack private AI document assistant using **RAG**, enabling users to upload PDFs and query their content using semantic retrieval and grounded LLM responses.  
> • Implemented **JWT authentication, user-level document isolation, PDF ingestion, embeddings, Chroma vector search, and source/page-aware responses** using FastAPI and LangChain.  
> • Integrated **Ollama Qwen3 8B and nomic-embed-text** for local LLM inference and embeddings, avoiding dependency on paid proprietary AI APIs.  
> • Deployed the React/Vite frontend on **Vercel** and exposed the FastAPI backend through **Cloudflare Tunnel** for remote access.

That is strong enough to be one of the **main projects on your resume**, especially because it demonstrates backend + AI + system architecture rather than just CRUD.
