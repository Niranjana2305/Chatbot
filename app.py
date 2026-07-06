import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from datetime import datetime, date
from typing import Optional, List
from sqlmodel import create_engine, SQLModel, Session, Field, select
import uuid
from langchain_core.tools import tool

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")

class HabitTrackerModel(SQLModel, table = True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index = True)
    description: Optional[str] = None
    created_at: date = Field(default_factory = date.today)
    streak: int = Field(default=0)
    last_checked_in: Optional[date] = None
    frequency_days: int = Field(default=1)

DATABASE_URL = "sqlite:///habits.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

init_db()

def verify_and_update_streak(habit: HabitTrackerModel, session: Session) ->None:
    if habit.last_checked_in is None:
        return
    today = date.today()
    if (today - habit.last_checked_in).days > habit.frequency_days:
        habit.streak = 0
        session.add(habit)
        session.commit()

@tool
def add_habit(name:str, frequency_days:int = 1, description: Optional[str]= None) -> str:
    """
    Add a new habit to the database and start tracking its streak.
    Always clarify or pass the frequency_days integer (e.g., 1 for daily, 2 for every two days, 7 for weekly, 30 for monthly).
    """
    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(HabitTrackerModel.name == name)
        existing = session.exec(statement).first()
        if existing:
            return f"Habit '{name}' already exists in your tracker."
        else:
            new_habit = HabitTrackerModel(name=name, frequency_days = frequency_days, description=description)
            session.add(new_habit)
            session.commit()
            return f"Great! I've added '{name}' to your habit tracker with a frequency of {frequency_days} days. Let's build this streak!"
        
@tool
def list_habits() ->str:
    """List all habits the user is currently tracking. Always use this tool when the user asks to see their habits."""
    with Session(engine) as session:
        statement = select(HabitTrackerModel)
        habits = session.exec(statement).all()

        if not habits:
            return "You don't have any habits tracked yet! Let's add one."
        
        response = "Here are your current habits: \n\n"
        for h in habits:
            verify_and_update_streak(h, session)
            last_checked = h.last_checked_in.strftime("%Y-%m-%d") if h.last_checked_in else "Never"
            response += f"- {h.name}: {h.description} (Streak: {h.streak}) (Last Checked: {last_checked})\n"
        return response
    
@tool
def log_checkin(name:str)->str:
    """Log a successful check-in for a specific habit by name."""
    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(HabitTrackerModel.name == name)
        habit = session.exec(statement).first()

        if not habit:
            return f"I don't see a habit named '{name}'. Please make sure to add it first."
        
        verify_and_update_streak(habit, session)
        today = date.today()
        
        if habit.last_checked_in == today:
            return f"You already logged a check-in for '{name}' today! Keep up the great work!"
        
        habit.streak += 1
        habit.last_checked_in = today
        session.add(habit)
        session.commit()
        
        return f"Streak updated! You've now completed '{name}' for {habit.streak} consecutive days. Keep it going!"

HABIT_TOOLS = [add_habit, list_habits, log_checkin]

def clean_bot_output(raw_text: str) -> str:
        if "</think>" in raw_text:
            return raw_text.split("</think>")[-1].strip()
        return raw_text


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
            trigger=("messages", 11),
            keep=("messages", 4)
        )
    ]
)

if __name__ == "__main__":
    session_thread_id = f"user-session-{uuid.uuid4().hex[:8]}"

    config = {"configurable": {"thread_id": session_thread_id}}
    print("--------------------------------")
    print("Habit Builder and Accountability Coach")
    print("--------------------------------")
    print("Chat with bot and type 'exit' to quit")
    print("--------------------------------")

    user_input = input("\nYou: ")

    while user_input.strip().lower() != "exit":
        if user_input.strip():
            inputs = {"messages": [HumanMessage(content=user_input)]}
            response = chatbot.invoke(inputs, config)
            clean_response = clean_bot_output(response['messages'][-1].content)
            print(f"Coach: {clean_response}")
        user_input = input("\nYou: ")

    print("Goodbye!")
        


