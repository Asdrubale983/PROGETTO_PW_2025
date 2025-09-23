from fastapi import APIRouter
from app.data.db import SessionDep

from app.models.user import User, UserPublic
from app.models.event import Event, EventPublic
from app.models.registration import Registration
from sqlmodel import select

router = APIRouter(prefix="/registrations")



@router.get("/")
def get_all_registrations(session: SessionDep) -> list[Registration]:
    """ Ritorna la lista di registrazioni """
    registrations = session.exec(select(Registration)).all()
    return registrations




"""DA IMPLEMENTARE: """


# @router.delete("/")
""" Elimina una registrazione dati username e event_id"""
def delete_registration(
        session: SessionDep,
        username: str,
        event_id: int):
    pass