from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from todos.schemas import Todo
from todos.db import (
    add_todos,
    get_todos,
    update_todo,
    delete_todo,
    create_db_and_tables,
)

app = FastAPI()


student_1 = Todo(
    title="Watch Lectures",
    description="Watch FastAPI lectures on YouTube",
    is_completed=False,
)
student_2 = Todo(
    title="Drink Chai",
    description="Make and drink a cup of chai",
    priority=4,
    is_completed=True,
)


@app.post("/add_todo")
def add_todos():
    return add_todos([student_1, student_2])


@app.get("/get_todo")
def get_todos():
    return get_todos()


@app.put("/update_todo/{id}")
def update_todos():
    return update_todo(id)


@app.delete("/delete_todo/{id}")
def delete_todos():
    return delete_todo(id)


# ----------------------------------------- Purana Code -----------------------


# This is the in-memory list to store student data
students = [
    {"name": "Tayyab", "RollNo": 520},
    {"name": "Ali", "RollNo": 521},
    {"name": "Bilal", "RollNo": 522},
    {"name": "Abubakar", "RollNo": 523},
]


class Student(BaseModel):
    name: str
    RollNo: int


@app.get("/")
def read_root():
    return {"message": "Hello World"}


"""
id : Path parameter
cnic, city : Query parameters
student — a Student Pydantic model : Body parameter
"""


@app.get("/todos/{id}")
def read_todo(id: int, cnic: str, city: str, student: Student):
    return student


@app.get("/students")
def read_students(name: str = None, RollNo: int = None):
    if name is None and RollNo is None:
        return students
    for std in students:
        if name == std.get("name") and RollNo == std.get("RollNo"):
            return {"name": name, "RollNo": RollNo}
    return {"message": "Student not found"}


@app.post("/add_student")
def add_student(student: Student):
    new_student = {"name": student.name, "RollNo": student.RollNo}
    students.append(new_student)
    return students


@app.delete("/delete_student")
def delete_student(name: str, RollNo: int):
    for std in students:
        if name == std.get("name") and RollNo == std.get("RollNo"):
            students.remove(std)
            return students
    return {"message": "Student not found"}


@app.get("/todos")
def read_todos():
    return {
        "todos": [
            "Drink Chai",
            "Read the documentation",
            "Write code",
            "Test the application",
        ]
    }


def start():
    create_db_and_tables()
    uvicorn.run("todos.main:app", host="127.0.0.1", port=8080, reload=True)
