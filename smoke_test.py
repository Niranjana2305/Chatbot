import uuid
from langchain_core.messages import HumanMessage
from app import chatbot, clean_bot_output

def smoke_test():
    test_thread_id = f"smoke-test-{uuid.uuid4().hex[:6]}"
    test_config = {"configurable": {"thread_id": test_thread_id}}
    
    test_phrases = [
        "Hello coach!", "I want to track reading.", "I read for 20 minutes.",
        "Check-in complete.", "Just keeping up.", "What's my streak?",
        "Doing great today.", "Another day down.", "Checking in again.",
        "Almost done."
    ]
    
    for t in test_phrases:
        # Fixed: Changed 'agent' to 'chatbot' and 'config' to 'test_config' to match your setup
        response = chatbot.invoke({"messages": [HumanMessage(content=t)]}, test_config)
        
        # Prints the clean reply so you can track the conversation flow
        clean = clean_bot_output(response["messages"][-1].content)
        print(f"You: {t}")
        print(f"Coach: {clean}")
        
        # Fixed: Corrected the syntax for printing the length of the message array
        print(f"Total messages in history buffer: {len(response['messages'])}")
        print("-" * 50)

if __name__ == "__main__":
    smoke_test()