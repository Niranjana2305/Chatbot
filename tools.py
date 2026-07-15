from typing import Optional
from sqlmodel import Session, select, func
from models import HabitTrackerModel, engine, verify_and_update_streak
from langchain_core.tools import tool
from datetime import date

@tool
def add_habit(name:str, frequency_days:int = 1, description: Optional[str]= None) -> str:
    """
    Add a new habit to the database and start tracking its streak.
    Always clarify or pass the frequency_days integer (e.g., 1 for daily, 2 for every two days, 7 for weekly, 30 for monthly).
    """
    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(func.lower(HabitTrackerModel.name) == name.strip().lower())
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
        statement = select(HabitTrackerModel).where(func.lower(HabitTrackerModel.name) == name.strip().lower())
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