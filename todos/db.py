from sqlmodel import SQLModel, create_engine, Session, select
from todos.schemas import Todos
import os

connection_string = os.getenv("DB_URI")
print(f"Using database connection string: {connection_string}")
connection_engine = create_engine(connection_string)


def create_db_and_tables():
    if connection_engine.has_table(Todos.__tablename__):
        print("Tables already exist.")
    SQLModel.metadata.create_all(connection_engine)


def add_todos(todo_list):
    with Session(connection_engine) as session:
        for todo in todo_list:
            session.add(todo)
        session.commit()
    return {"message": "Todos added successfully"}


def get_todos():
    with Session(connection_engine) as session:
        statement = select(Todos)
        results = session.exec(statement)
        todos_data = results.all()
    return todos_data
