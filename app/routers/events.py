from fastapi import APIRouter, Path, HTTPException
from app.data.db import SessionDep

from app.models.event import Event, EventCreate, EventPublic
from app.models.registration import Registration
from app.models.user import User, UserPublic
from sqlmodel import select, delete
from typing import Annotated

router = APIRouter(prefix="/events")


@router.get("/")
def get_all_events(session: SessionDep):

    """ Ritorna la lista di eventi """
    events = session.exec(select(Event)).all()
    return events



@router.post("/")
def add_event(session: SessionDep, event: EventCreate):

    """ Crea un nuovo evento """
    session.add(Event.model_validate(event))
    session.commit()
    return "Event successfully created"



# da testare
@router.delete("/")
def delete_all_events(session: SessionDep):

    """ Elimina la lista di eventi """
    session.exec(delete(Event))
    session.commit()
    return "All books successfully deleted"



@router.get("/{id}")
def get_event_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to get")]
    ) -> EventPublic:

    """ Ritorna un evento dato l'ID """
    event = session.get(Event, id)
    if event:
        return event
    else: 
        raise HTTPException(status_code=404, detail="Event not found")



@router.put("/{id}")
def update_event(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to get")],
    new_event: EventCreate
    ):

    """ Aggiorna un evento dato l'ID """
    event = session.get(Event, id)
    if not event: 
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.commit()
    return "Event updated successfully"



@router.delete("/{id}")
def delete_event(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to get")]
    ):

    """ Elimina un evento dato l'ID """
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return ("Event successfully deleted")
    


@router.post("/{id}/register")
def create_registration(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the event to get")],
    user: User
    ):

    """ Registra un utente a un dato evento """
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    search_user = session.get(User, user.username)
    if not search_user:
        raise HTTPException(status_code=404, detail="User not found")

    registration = Registration(username=user.username,
                                event_id=id)
    session.add(Registration.model_validate(registration))
    session.commit()
    return "Registration completed successfully"