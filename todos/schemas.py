from sqlmodel import SQLModel, Field


class TodoBase(SQLModel):
    title: str
    description: str
    priority: int | None = None
    is_completed: bool = False


class Todo(TodoBase, table=True):
    id: int = Field(default=None, primary_key=True)


class CreateTodo(TodoBase):
    pass


class UpdateTodo(SQLModel):
    title: str | None
    description: str | None
    priority: int | None = None
    is_completed: bool | None = False
