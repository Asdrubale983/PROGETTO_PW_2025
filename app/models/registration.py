"""from sqlmodel import SQLModel, Field


class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username")
    event_id: int = Field(primary_key=True, foreign_key="event.id")
"""



from sqlmodel import SQLModel, Relationship, Field

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username", ondelete="CASCADE")
    user_attr: User | None = Relationship(back_populates="registration_attr")

    event_id: int = Field(primary_key=True, foreign_key="event.id")
    event_attr: Event | None = Relationship(back_populates="registration_attr")
