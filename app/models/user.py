from sqlmodel import SQLModel, Field, Relationship


class BaseUser(SQLModel):
    # superclasse con attributi comuni 
    name: str
    email: str
"""
class User(BaseUser, table = True):
    # classe ORM 
    username: str = Field(primary_key=True)"""

from typing import List

class User(BaseUser, table = True):
    username: str = Field(primary_key=True)

    registration_attr: list["Registration"] = Relationship(back_populates="user_attr", cascade_delete=True)



class CreateUser(BaseUser):
    # schema per creare un nuovo utente
    username: str

class UserPublic(BaseUser):
    # schema per restituire i dati dell'utente
    username: str

