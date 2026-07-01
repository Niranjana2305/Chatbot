import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

load_dotenv()

chatbot = create_agent(
    model="groq:qwen/qwen3-32b",
    tools=[],
    checkpointer=InMemorySaver(),
    system_prompt="You are a warm, helpful, and intelligent chatbot assistant.",
    middleware=[
        SummarizationMiddleware(
            model="groq:qwen/qwen3-32b",
            trigger=("messages", 10),
            keep=("messages", 4)
        )
    ]
)

config = {"configurable": {"thread_id": "test-thread-1"}}
print("--------------------------------")
print("Langchain Chatbot")
print("--------------------------------")
print("Chat with bot and type 'exit' to quit")
print("--------------------------------")
user_input = input("\nYou: ")
while user_input.strip().lower() != "exit":
    if user_input.strip():
        inputs = {"messages": [HumanMessage(content=user_input)]}
        response = chatbot.invoke(inputs, config)
        raw_content = response['messages'][-1].content
        if "</think>" in raw_content:
            raw_content = raw_content.split("</think>")[-1].strip()

        print(f"Chatbot: {raw_content}")
    user_input = input("\nYou: ")

print("Goodbye!")
    


