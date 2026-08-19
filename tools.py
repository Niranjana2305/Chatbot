from typing import Optional
from sqlmodel import Session, select, func
from models import HabitTrackerModel, engine, verify_and_update_streak
from langchain_core.tools import tool
from datetime import date
from rag import search_health_knowledge_base  

@tool
def save_user_profile(user_id: str, key: str, value: str) -> str:
    """Save long-term user facts across chat sessions (e.g., key='motivation', value='wants more energy for kids')."""
    if not user_id or not key or not value:
        return "Error: missing user_id, key, or value."
    
    from agent import store
    namespace = ("users", user_id, "profile")
    store.put(namespace, key, {"data": value})
    return f"Successfully saved memory '{key}' for user '{user_id}'."

@tool
def get_user_profile(user_id: str) -> str:
    """Retrieve all saved long-term profile memories for a given user_id."""
    from agent import store
    namespace = ("users", user_id, "profile")
    items = store.search(namespace)
    
    if not items:
        return f"No long-term memories found for user '{user_id}'."
    
    records = [f"- {item.key}: {item.value.get('data')}" for item in items]
    return f"Long-term profile for user '{user_id}':\n" + "\n".join(records)

@tool
def add_habit(user_id:str, name:str, frequency_days:int = 1, description: Optional[str]= None) -> str:
    """
    Add a new habit to the database for a specific user_id and start tracking its streak.
    Always clarify or pass the frequency_days integer (e.g., 1 for daily, 2 for every two days, 7 for weekly, 30 for monthly).
    """
    if not user_id:
        return "Error: User ID is required."

    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(HabitTrackerModel.user_id == user_id, func.lower(HabitTrackerModel.name) == name.strip().lower())
        existing = session.exec(statement).first()
        if existing:
            return f"Habit '{name}' already exists in your tracker."
        else:
            new_habit = HabitTrackerModel(user_id = user_id,name=name.strip(), frequency_days = frequency_days, description=description)
            session.add(new_habit)
            session.commit()
            return f"Great! I've added '{name}' to your habit tracker with a frequency of {frequency_days} days. Let's build this streak!"
        
@tool
def list_habits(user_id:str) ->str:
    """ List all active habits for a specific user_id.
    Always use this tool when the user asks to see their habits.
    """
    if not user_id:
        return "Error: User ID is required."

    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(HabitTrackerModel.user_id == user_id)
        habits = session.exec(statement).all()

        if not habits:
            return f"You don't have any habits tracked yet '{user_id}'! Let's add one."
        
        response = "Here are your current habits for user '{user_id}': \n\n"
        for h in habits:
            verify_and_update_streak(h, session)
            last_checked = h.last_checked_in.strftime("%Y-%m-%d") if h.last_checked_in else "Never"
            desc_str = f": {h.description}" if h.description else ""
            response += f"- {h.name}{desc_str} (Streak: {h.streak}) (Last Checked: {last_checked})\n"
        return response 

@tool
def log_checkin(user_id:str, name:str)->str:
    """Log a successful check-in for a specific habit by name for a given user_id"""
    if not user_id:
        return "Error: User ID is required."

    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(HabitTrackerModel.user_id == user_id, func.lower(HabitTrackerModel.name) == name.strip().lower())
        habit = session.exec(statement).first()

        if not habit:
            return f"I don't see a habit named '{name}' for user '{user_id}'. Please make sure to add it first."
        
        verify_and_update_streak(habit, session)
        today = date.today()
        
        if habit.last_checked_in == today:
            return f"You already logged a check-in for '{name}' today! Keep up the great work!"
        
        habit.streak += 1
        habit.last_checked_in = today
        session.add(habit)
        session.commit()
        
        return f"Streak updated! You've now completed '{name}' for {habit.streak} consecutive days. Keep it going!"

HABIT_TOOLS = [add_habit, list_habits, log_checkin, search_health_knowledge_base, save_user_profile, get_user_profile]
