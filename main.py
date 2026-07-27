from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, ToolMessage
from agent import chatbot, clean_bot_output
from contextlib import asynccontextmanager
from models import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    answer_type: str = "direct"
    retrieved_content: list[str] = []

@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.post('/chat', response_model=ChatResponse)
def chat_message(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    config = {"configurable": {"thread_id": request.thread_id}}
    user_input = {"messages": [HumanMessage(content=request.message)]}
    result = chatbot.invoke(user_input, config)

    all_messages = result.get('messages', [])
    if not all_messages:
        raise HTTPException(status_code=500, detail="No response from chatbot")
        
    raw_text = all_messages[-1].content
    cleaned = clean_bot_output(raw_text)

    answer_type = "direct"
    retrieved_content = []

    # 1. Find the index of the MOST RECENT HumanMessage (the current turn)
    last_human_idx = -1
    for idx in range(len(all_messages) - 1, -1, -1):
        if isinstance(all_messages[idx], HumanMessage):
            last_human_idx = idx
            break

    # 2. Inspect ONLY messages generated in this current turn (after the last HumanMessage)
    if last_human_idx != -1:
        current_turn_messages = all_messages[last_human_idx:]
        for msg in current_turn_messages:
            if isinstance(msg, ToolMessage):
                tool_name = getattr(msg, "name", "") or ""
                if "search_health" in tool_name or "knowledge_base" in tool_name:
                    content = str(msg.content).strip()
                    if content and not content.startswith("No specific health") and not content.startswith("Health knowledge base is currently unavailable"):
                        answer_type = "rag"
                        retrieved_content.append(content)

    return ChatResponse(
        response=cleaned, 
        answer_type=answer_type, 
        retrieved_content=retrieved_content
    )