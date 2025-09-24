from sqlmodel import SQLModel, Relationship, Field
from datetime import datetime

""" Definizione delle classi relative agli utenti: """

class BaseUser(SQLModel):
    # superclasse con attributi comuni 
    name: str
    email: str

class User(BaseUser, table = True):
    username: str = Field(primary_key=True)

    registration_attr: list["Registration"] = Relationship(
        back_populates="user_attr", cascade_delete=True)
    
class CreateUser(BaseUser):
    # schema per creare un nuovo utente
    username: str

class UserPublic(BaseUser):
    # schema per restituire i dati dell'utente
    username: str


""" Definizione delle classi relative agli eventi: """

class BaseEvent(SQLModel):
    # superclasse con attributi comuni
    title: str
    description: str
    date: datetime
    location: str

class Event(BaseEvent, table=True):
    id: int | None = Field(default=None, primary_key=True)
    registration_attr: list["Registration"] = Relationship(
        back_populates="event_attr", cascade_delete=True)
    
class EventCreate(BaseEvent):
    # schema per creare un nuovo evento
    pass

class EventPublic(BaseEvent):
    # schema per restituire le info di un evento
    id: int 
    pass


""" Definizione della classe relativa alle registrazioni: """

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username", ondelete="CASCADE")
    user_attr: User | None = Relationship(back_populates="registration_attr")

    event_id: int = Field(primary_key=True, foreign_key="event.id", ondelete="CASCADE")
    event_attr: Event | None = Relationship(back_populates="registration_attr")