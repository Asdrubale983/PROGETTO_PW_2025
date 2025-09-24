from fastapi import APIRouter, HTTPException, Query
from app.data.db import SessionDep
from app.models.registration import Registration
from sqlmodel import select
from typing import Annotated

router = APIRouter(prefix="/registrations")



@router.get("/")
def get_all_registrations(session: SessionDep) -> list[Registration]:
    """ Ritorna la lista di registrazioni """
    registrations = session.exec(select(Registration)).all()
    return registrations



@router.delete("/")
def delete_registration(
    session: SessionDep,
    username: Annotated[str, Query(description="username dell'utente di cui cancellare la registrazione")],
    event_id: Annotated[int, Query(description="ID dell'evento di cui cancellare la registrazione")]
    ):
    
    """ Elimina una registrazione dati username e event_id """
    registration = Registration(username=username, event_id=event_id)
    registration = session.get(Registration, (username, event_id))
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    session.delete(registration)
    session.commit()
    return "Registration successfully deleted"