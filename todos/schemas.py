from sqlmodel import SQLModel, Field

class Todos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: int | None = None
    is_completed: bool = False
