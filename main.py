from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel
from agent import chatbot, clean_bot_output
from models import init_db
from output_guard import apply_output_guardrail

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

    config = {
        "configurable": {
            "thread_id": request.thread_id,
            "user_id": request.user_id,
        }
    }
    
    formatted_input = f"<user_prompt>\n[User ID: {request.user_id}]\n{request.message}\n</user_prompt>"
    user_input = {"messages": [HumanMessage(content=formatted_input)]}
    try:
        current_state = chatbot.get_state(config)
        history_len_before = len(current_state.values.get("messages", []))
    except Exception:
        history_len_before = 0
    result = chatbot.invoke(user_input, config)
    all_messages = result.get("messages", [])
    if not all_messages:
        raise HTTPException(status_code=500, detail="No response from chatbot")

    new_messages = all_messages[history_len_before:]
    answer_type = "direct"
    retrieved_context = []
    for msg in new_messages:
        if (
            isinstance(msg, ToolMessage)
            and getattr(msg, "name", None) == "search_health_knowledge_base"
        ):
            answer_type = "rag"
            retrieved_context.append(str(msg.content))

    ai_messages = [m for m in all_messages if isinstance(m, AIMessage)]
    if not ai_messages:
        raise HTTPException(
            status_code=500, detail="Chatbot failed to generate an AI response."
        )

    last_ai_msg = ai_messages[-1]
    raw_text = ""

    if isinstance(last_ai_msg.content, str):
        raw_text = last_ai_msg.content
    elif isinstance(last_ai_msg.content, list):
        text_parts = []
        for block in last_ai_msg.content:
            if isinstance(block, str):
                text_parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
        raw_text = "\n".join(text_parts)
    elif isinstance(last_ai_msg.content, dict):
        raw_text = last_ai_msg.content.get("text", "")
    cleaned = clean_bot_output(raw_text)
    if not cleaned or not cleaned.strip():
        cleaned = raw_text.strip() or "No output generated."
    guarded_response = apply_output_guardrail(cleaned)
  
    return ChatResponse(
        response=guarded_response,
        answer_type=answer_type,
        retrieved_context=retrieved_context,
    )
