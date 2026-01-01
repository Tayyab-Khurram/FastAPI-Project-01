from fastapi import HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from todos.schemas import Todo, UpdateTodo
import os

connection_string = os.getenv("DB_URI")
print(f"Using database connection string: {connection_string}")
connection_engine = create_engine(connection_string)


def create_db_and_tables():
    if connection_engine.has_table(Todo.__tablename__):
        print("Table already exist.")
        return
    SQLModel.metadata.create_all(connection_engine)


def add_todos(todo: Todo):
    with Session(connection_engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return {"status": 200, "todo": todo}


def get_todos():
    with Session(connection_engine) as session:
        statement = select(Todo)
        results = session.exec(statement)
        todos_data = results.all()
    return todos_data


def update_todo(id: int, todo: UpdateTodo):
    with Session(connection_engine) as session:
        statement = select(Todo).where(Todo.id == id)
        results = session.exec(statement)
        if not results:
            raise HTTPException(status_code=404, detail="No Todo found against this id")
        todo_data = results.one()
        todo_data.title = todo.title if todo.title is not None else todo_data.title
        todo_data.description = (
            todo.description if todo.description is not None else todo_data.description
        )
        todo_data.priority = (
            todo.priority if todo.priority is not None else todo_data.priority
        )
        todo_data.is_completed = (
            todo.is_completed
            if todo.is_completed is not None
            else todo_data.is_completed
        )
        session.add(todo_data)
        session.commit()
        session.refresh(todo_data)
        return {"status": 200, "todo": todo_data}
