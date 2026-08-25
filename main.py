from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import get_safe_response
from models import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    user_id: str
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    answer_type: str = "direct"
    retrieved_context: list[str] = []

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat_message(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    try:
        res = get_safe_response(
            user_id=request.user_id,
            thread_id=request.thread_id,
            message=request.message,
        )
        return ChatResponse(
            response=res["response"],
            answer_type=res["answer_type"],
            retrieved_context=res["retrieved_context"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
