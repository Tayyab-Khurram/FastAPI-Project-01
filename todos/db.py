from fastapi import HTTPException
from fastapi.responses import FileResponse
from sqlmodel import SQLModel, create_engine, Session, select
from todos.schemas import Todo, UpdateTodo, CreateTodo
import os
import csv

connection_string = os.getenv("DB_URI")
print(f"Using database connection string: {connection_string}")
connection_engine = create_engine(connection_string)


def create_db_and_tables():
    SQLModel.metadata.create_all(connection_engine)


def add_todo(todo: CreateTodo):
    with Session(connection_engine) as session:
        db_todo = Todo.model_validate(todo)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return {"status": 200, "todo": db_todo}


def get_todo(id: int):
    with Session(connection_engine) as session:
        todo = session.get(Todo, id)
        if not todo:
            raise HTTPException(status_code=404, detail="No Todo found against this id")
        return {"status": 200, "todo": todo}


def update_todo(id: int, todo: UpdateTodo):
    with Session(connection_engine) as session:
        result = session.get(Todo, id)
        if not result:
            raise HTTPException(status_code=404, detail="No Todo found against this id")
        db_todo = todo.model_dump(exclude_unset=True)
        result.sqlmodel_update(db_todo)
        session.add(result)
        session.commit()
        session.refresh(result)
        return {"status": 200, "todo": result}


def delete_todo(id: int):
    with Session(connection_engine) as session:
        result = session.get(Todo, id)
        if not result:
            raise HTTPException(status_code=404, detail="No Todo found against this id")
        session.delete(result)
        session.commit()
        return {"status": 200, "todo": result}


def get_all_todos():
    with Session(connection_engine) as session:
        statement = select(Todo).order_by(Todo.id)
        todos = session.exec(statement).all()
        todos_dict = [todo.model_dump() for todo in todos]
        
        if not todos_dict:
            print("No todos found")
            return
        
        fieldnames = todos_dict[0].keys()
        filename = "all_todos.csv"

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(todos_dict)

        return FileResponse(
            path=filename,
            filename="all_todos.csv",
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=all_todos.csv"
            }
        )