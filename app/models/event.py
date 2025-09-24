from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class BaseEvent(SQLModel):
    # superclasse con attributi comuni
    title: str
    description: str
    date: datetime
    location: str
"""
class Event(BaseEvent, table = True):
    # classe ORM
    id: int | None = Field(default=None, primary_key=True)
"""

from typing import List
from datetime import datetime

class Event(BaseEvent, table=True):
    id: int | None = Field(default=None, primary_key=True)
    registration_attr: list["Registration"] = Relationship(back_populates="event_attr", cascade_delete=True)


class EventCreate(BaseEvent):
    # schema per creare un nuovo evento
    pass

class EventPublic(BaseEvent):
    # schema per restituire le info di un evento
    id: int 
    pass

