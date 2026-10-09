# Codebase Whisperer 🤖

A Self-Reflecting Agentic RAG (Retrieval-Augmented Generation) pipeline designed to deeply understand and chat with your codebase or document folders. 

Built with **LangGraph**, **FastAPI**, **Streamlit**, and **ChromaDB**.

## 🏗️ Architecture

This project uses an advanced **Corrective RAG (CRAG)** architecture to prevent hallucinations and ensure high-quality answers:

1. **Dynamic Ingestion (`ingestion.py`)**: Automatically detects file types (`.py`, `.js`, `.html`, etc.), dynamically routes them to the correct Language Parsers, splits them into semantic chunks, and embeds them into a local **ChromaDB** vector store using HuggingFace sentence-transformers.
2. **The LangGraph Brain (`graph.py`)**: A state-machine workflow that:
   - Retrieves relevant documents.
   - **Grades** the documents (Self-Reflection) using a strict LLM to filter out irrelevant context.
   - Uses **Conditional Edge Routing** to skip generation if no relevant documents survive the grader.
   - Generates the final answer using the filtered context.
3. **The API (`api.py`)**: A **FastAPI** backend that wraps the LangGraph workflow into a scalable `/chat` POST endpoint with Pydantic type validation.
4. **The Frontend (`ui.py`)**: A sleek **Streamlit** chat interface that communicates with the FastAPI backend.

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed and your virtual environment activated. You will also need a free API key from [Groq](https://console.groq.com/).

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_api_key_here
```

### Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 1. Ingest your Codebase
Run the ingestion script to parse your codebase and build the vector database:
```bash
python ingestion.py
```

### 2. Start the Backend API
Start the FastAPI server (runs on port 8000 by default):
```bash
uvicorn api:app --reload
```

### 3. Start the Chat UI
In a separate terminal, run the Streamlit frontend:
```bash
streamlit run ui.py
```

## 🐳 Docker Deployment
This project is fully containerized and ready for deployment on platforms like Render or Railway. 
It uses a `start.sh` script to run both FastAPI and Streamlit concurrently.
```bash
docker build -t codebase-whisperer .
docker run -p 8000:8000 -p 8501:8501 codebase-whisperer
```
