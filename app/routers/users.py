from fastapi import APIRouter, Path, HTTPException
from app.data.db import SessionDep
from typing import Annotated
from app.models.models import User, UserPublic, CreateUser, Registration
from sqlmodel import select, delete


router = APIRouter(prefix="/users")



@router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:

    """ Ritorna la lista di utenti """
    users = session.exec(select(User)).all()
    return users



@router.post("/")
def add_user(session: SessionDep, user: CreateUser):

    """ Crea un nuovo utente """
    session.add(User.model_validate(user))
    session.commit()
    return "User successfully created!"



@router.delete("/")
def delete_all_users(session: SessionDep):

    """ Elimina la lista di utenti """
    session.exec(delete(User))

    # Cancella anche l'interità della tabella Registration
    session.exec(delete(Registration))

    session.commit()
    return "All users successfully deleted!"



@router.get("/{username}")
def get_user_by_username(
    session: SessionDep,
    username: Annotated[str, 
            Path(description="The username of the user to get")]
    ) -> UserPublic:

    """ Ritorna un utente dato l'username """
    user = session.get(User, username)
    if user: 
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")



@router.delete("/{username}")
def delete_user(
    session: SessionDep,
    username: Annotated[str,
            Path(description="The username of the user to delete")]):
    
    """ Elimina un utente dato l'username """
    user = session.get(User, username)
    if user:
        session.delete(user)
        session.commit()
        return "User successfully deleted"
    else: 
        raise HTTPException(status_code=404, detail="User not found")
