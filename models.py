from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select

DATABASE_URL = "sqlite:///habits.db"
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
    )

class HabitTrackerModel(SQLModel, table = True):
    id:Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index = True)
    name: str = Field(index = True)
    description: Optional[str] = None
    created_at: date = Field(default_factory = date.today)
    streak: int = Field(default=0)
    last_checked_in: Optional[date] = None
    frequency_days: int = Field(default=1)

def init_db():
    SQLModel.metadata.create_all(engine)

def verify_and_update_streak(habit: HabitTrackerModel, session: Session) ->None:
    if habit.last_checked_in is None:
        return
    today = date.today()
    if (today - habit.last_checked_in).days > habit.frequency_days:
        habit.streak = 0
        session.add(habit)
        session.commit()
        session.refresh(habit)

def delete_habit_db(user_id: str, name: str) -> bool:
    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(
            HabitTrackerModel.user_id == user_id,
            HabitTrackerModel.name.ilike(name),
        )
        habit = session.exec(statement).first()
        if not habit:
            return False
        session.delete(habit)
        session.commit()
        return True


def update_habit_db(
    user_id: str,
    name: str,
    frequency_days: Optional[int] = None,
    description: Optional[str] = None,) -> Optional[HabitTrackerModel]:

    with Session(engine) as session:
        statement = select(HabitTrackerModel).where(
            HabitTrackerModel.user_id == user_id,
            HabitTrackerModel.name.ilike(name),
        )
        habit = session.exec(statement).first()
        if not habit:
            return None
        if frequency_days is not None:
            habit.frequency_days = frequency_days
        if description is not None:
            habit.description = description

        session.add(habit)
        session.commit()
        session.refresh(habit)
        return habit
        
