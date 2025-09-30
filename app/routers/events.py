from fastapi import APIRouter, Path, HTTPException
from app.data.db import SessionDep
from app.models.models import Event, EventCreate, EventPublic, Registration, User, UserPublic
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



@router.delete("/")
def delete_all_events(session: SessionDep):

    """ Elimina la lista di eventi """
    session.exec(delete(Event))

    # Cancella anche l'interità della tabella Registration
    session.exec(delete(Registration))
    
    session.commit()
    return "All events successfully deleted"

    


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
    user: UserPublic
    ):

    """ Registra un utente a un dato evento """
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
   
    search_user = session.get(User, user.username)

    if not search_user:  # controlla che l'username dell'utente sia nel DB
        raise HTTPException(status_code=404, detail="User not found")
    
    # controlla che nome e email corrispondano
    if search_user.name != user.name or search_user.email != user.email:
        raise HTTPException(status_code=400, detail="Bad Request")


    registration = Registration(username=search_user.username,
                                event_id=event.id,
                                user_attr = search_user,
                                event_attr = event)
    session.add(Registration.model_validate(registration))
    session.commit()

    return "Registration completed successfully"