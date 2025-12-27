from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


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
