from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config

from app.models.models import Event, User, Registration


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)

    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:

            # Creazione di utenti fittizi:
            user_list = []
            for i in range(10):
                user = User(name = f.name(), 
                            username=f.user_name(), 
                            email=f.email())
                user_list.append(user)
                session.add(user)
            session.commit()

            # Creazione di eventi fittizi:
            event_list = []
            for i in range(10):
                event = Event(title = f.sentence(nb_words=2), 
                              description = f.sentence(nb_words=4), 
                              date = f.date_time_this_month(), 
                              location = f.city())
                event_list.append(event)
                session.add(event)
            session.commit()

            
            # Creazione di registrazioni fittizie:
            for i in range(10):
                registration = Registration(username=user_list[i].username,
                                            event_id=event_list[i].id)
                session.add(registration)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
