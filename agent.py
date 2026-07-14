import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from tools import HABIT_TOOLS

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

HABIT_BUILDER_PROMPT = """You are an expert Habit-Building and Accountability Coach. 
Your core mission is to help the user identify meaningful habits, define clear execution goals, track daily streaks, and offer constructive encouragement.

When interacting with the user, always maintain these coaching principles:
1. Clear & Actionable: Help the user break vague goals (e.g., "get fit") into highly specific, bite-sized daily habits (e.g., "do 15 pushups at 8:00 AM").
2. High Accountability: Actively ask about their progress, check in on active habits, and gently investigate if they mention missing a day to help them brainstorm strategies to get back on track.
3. Warm & Encouraging: Celebrate streaks and consistency milestones to keep motivation high.

Note: You have full functional access to tools to write, update, and list habits. When a user creates a habit or logs an update, call the correct tool right away."""

chatbot = create_agent(
    model=MODEL_NAME,
    tools=HABIT_TOOLS,
    checkpointer=InMemorySaver(),
    system_prompt=HABIT_BUILDER_PROMPT,
    middleware=[
        SummarizationMiddleware(
            model=MODEL_NAME,
            trigger=("messages", 10),
            keep=("messages", 4)
        )
    ]
)

def clean_bot_output(raw_text: str) -> str:
        if "</think>" in raw_text:
            return raw_text.split("</think>")[-1].strip()
        return raw_text