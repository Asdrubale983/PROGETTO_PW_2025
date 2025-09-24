from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    # superclasse con attributi comuni 
    name: str
    email: str

class User(BaseUser, table = True):
    # classe ORM 
    username: str = Field(primary_key=True)

class CreateUser(BaseUser):
    # schema per creare un nuovo utente
    username: str

class UserPublic(BaseUser):
    # schema per restituire i dati dell'utente
    username: str
