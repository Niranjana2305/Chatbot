from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
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
    answer_type: str 
    retrieved_context: list[str] = []

@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.post('/chat', response_model=ChatResponse)
def chat_message(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    config = {"configurable": {"thread_id": request.thread_id}}
    user_input = {"messages": [HumanMessage(content=request.message)]}
    
    try:
        current_state = chatbot.get_state(config)
        history_len_before = len(current_state.values.get("messages", []))
    except Exception:
        history_len_before = 0

    result = chatbot.invoke(user_input, config)

    all_messages = result.get('messages', [])
    if not all_messages:
        raise HTTPException(status_code=500, detail="No response from chatbot")

    new_messages = all_messages[history_len_before:]
    
    answer_type = "direct"
    retrieved_context = []

    for msg in new_messages:
        if isinstance(msg, ToolMessage) and getattr(msg, "name", None) == "search_health_knowledge_base":
            answer_type = "rag"
            retrieved_context.append(str(msg.content))

    ai_messages = [m for m in all_messages if isinstance(m, AIMessage)]
    if not ai_messages:
        raise HTTPException(status_code=500, detail="Chatbot failed to generate an AI response.")

    raw_text = ai_messages[-1].content
    
    if isinstance(raw_text, list):
        raw_text = "".join([str(block) for block in raw_text])

    cleaned = clean_bot_output(raw_text)

    if not cleaned or not cleaned.strip():
        cleaned = raw_text.strip() or "No output generated."

    return ChatResponse(
        response=cleaned,
        answer_type=answer_type,
        retrieved_context=retrieved_context
    )
