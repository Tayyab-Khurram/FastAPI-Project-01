from fastapi import FastAPI
import uvicorn

app = FastAPI()


students = [
    {"name": "Tayyab", "RollNo": 520},
    {"name": "Ali", "RollNo": 521},
    {"name": "Bilal", "RollNo": 522},
    {"name": "Abubakar", "RollNo": 523},
]


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/todos/{id}")
def read_todo(id: int, userName: str, RollNo: int):
    return {f"User {userName} with Roll No {RollNo} has a todo item with id {id}"}


@app.get("/students")
def read_students():
    return students


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
    uvicorn.run("todos.main:app", host="127.0.0.1", port=8080, reload=True)
