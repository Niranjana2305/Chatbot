import uuid
from langchain_core.messages import HumanMessage
from agent import chatbot, clean_bot_output
def smoke_test():
    test_thread_id = f"smoke-test-{uuid.uuid4().hex[:6]}"
    test_config = {"configurable": {"thread_id": test_thread_id}}
    
    test_phrases = [
        "Hello coach!", "I want to track reading.", "I read for 20 minutes.",
        "Check-in complete.", "Just keeping up.", "What's my streak?",
        "Doing great today.", "Another day down."
    ] 
    
    for t in test_phrases:
        response = chatbot.invoke({"messages": [HumanMessage(content=t)]}, test_config)
        
        clean = clean_bot_output(response["messages"][-1].content)
        print(f"You: {t}")
        print(f"Coach: {clean}")
        
        print(f"Total messages in history: {len(response['messages'])}")
        print("-" * 50)

if __name__ == "__main__":
    smoke_test()