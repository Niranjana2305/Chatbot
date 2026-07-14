import os
from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session


DATABASE_URL = "sqlite:///habits.db"
engine = create_engine(DATABASE_URL, echo=False)

class HabitTrackerModel(SQLModel, table = True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index = True)
    description: Optional[str] = None
    created_at: date = Field(default_factory = date.today)
    streak: int = Field(default=0)
    last_checked_in: Optional[date] = None
    frequency_days: int = Field(default=1)
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