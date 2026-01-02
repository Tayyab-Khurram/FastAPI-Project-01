from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    __tablename__ = "todo"
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: int | None = None
    is_completed: bool = False


class UpdateTodo(SQLModel):
    title: str | None
    description: str | None
    priority: int | None = None
    is_completed: bool | None = False
