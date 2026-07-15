from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent import chatbot, clean_bot_output
from contextlib import asynccontextmanager
from models import init_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app = FastAPI(lifespan = lifespan)

class ChatRequest(BaseModel):
    thread_id:str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.post('/chat', response_model= ChatResponse)
def chat_message(request:ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code = 400, detail = "Message content cannot be empty")

    config = {"configurable":{"thread_id": request.thread_id}}
    user_input = {"messages": [HumanMessage(content=request.message)]}
    result = chatbot.invoke(user_input, config)

    if 'messages' not in result or len(result['messages']) == 0:
        raise HTTPException(status_code=500, detail = "No response from chatbot")
        
    raw_text = result['messages'][-1].content
    cleaned = clean_bot_output(raw_text)

    return ChatResponse(response = cleaned)
