from typing import Optional
from sqlmodel import Session, select, func
from models import HabitTrackerModel, engine, verify_and_update_streak
from langchain_core.tools import tool
from datetime import date
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

@tool
def search_health_knowldedge_base(query:str) ->str:
    """
    Search the health and safety knowledge base for guidance on physical symptoms, 
    injuries, medical red flags, or exercise safety precautions.
    Args:
        query: The physical symptom, injury, or health concern to look up (e.g., 'chest pain', 'knee injury').
    """
    index_path = "faiss_index"
    
    if not os.path.exists(index_path):
        return "Sorry! I cannot help with that right now. The health and safety knowledge base is currently unavailable."
    
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            return "No relevant information found in the knowledge base."
        
        results = []
        for d in docs:
            source = d.metadata.get('source', 'Knowledge Base')
            results.append(f"Document Name: {source}\nContent: {d.page_content}\n")
        
        return "\n\n".join(results)
    
    except Exception as e:
        return f"Error loading or searching the knowledge base: {str(e)}"

@tool
def add_habit(habit_name:str, frequency_days:int = 1, description: Optional[str]= None) -> str:
    """
    Add a new habit to the database and start tracking its streak.
    Args:
        habit_name: The name of the habit to create (e.g., 'running', 'reading').
        frequency_days: Target frequency in days (1 for daily, 2 for every two days, 7 for weekly, 30 for monthly).
        description: Optional extra details or goals for the habit.
    """
    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(func.lower(HabitTrackerModel.name) == habit_name.strip().lower())
        existing = session.exec(statement).first()
        if existing:
            return f"Habit '{habit_name}' already exists in your tracker."
        else:
            new_habit = HabitTrackerModel(name=habit_name.strip(), frequency_days = frequency_days, description=description)
            session.add(new_habit)
            session.commit()
            return f"Great! I've added '{habit_name}' to your habit tracker with a frequency of {frequency_days} days. Let's build this streak!"
        
@tool
def list_habits() ->str:
    """
    List all habits the user is currently tracking in the database. 
    ALWAYS invoke this tool when the user asks to see, show, or list their habits.
    """
    with Session(engine) as session:
        statement = select(HabitTrackerModel)
        habits = session.exec(statement).all()

        if not habits:
            return "You don't have any habits tracked yet! Let's add one."
        
        response = "Here are your current habits: \n\n"
        
        for h in habits:
            verify_and_update_streak(h, session)
            last_checked = h.last_checked_in.strftime("%Y-%m-%d") if h.last_checked_in else "Never"
            desc = f": {h.description}" if h.description else ""
            response += f"- {h.name}{desc} (Streak: {h.streak}) (Last Checked: {last_checked})\n"
        return response
    
@tool
def log_checkin(habit_name:str)->str:
    """
    Log a successful check-in for a specific habit by name.
    Args:
        habit_name: The name of the habit to log a check-in for (e.g., 'running', 'biking').
    """
    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(func.lower(HabitTrackerModel.name) == habit_name.strip().lower())
        habit = session.exec(statement).first()

        if not habit:
            return f"I don't see a habit named '{habit_name}'. Please make sure to add it first."
        
        verify_and_update_streak(habit, session)
        today = date.today()
        
        if habit.last_checked_in == today:
            return f"You already logged a check-in for '{habit_name}' today! Keep up the great work!"
        
        habit.streak += 1
        habit.last_checked_in = today
        session.add(habit)
        session.commit()
        
        return f"Streak updated! You've now completed '{habit_name}' for {habit.streak} consecutive days. Keep it going!"

ALL_TOOLS = [add_habit, list_habits, log_checkin, search_health_knowldedge_base]