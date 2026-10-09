from fastapi import FastAPI
from pydantic import BaseModel
from graph import workflow

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def ask(request: ChatRequest):
    """
    Endpoint to ask a question about the codebase.
    """
    try:
        # Invoke the LangGraph workflow
        result = workflow.invoke({"question": request.question})
        
        # Return the generated answer
        return {
            "answer": result.get('generation', 'No answer generated'),
            "source_documents": [doc.metadata['source'] for doc in result.get('document', [])]
        }
    except Exception as e:
        return {"error": str(e)}