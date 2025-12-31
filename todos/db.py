from sqlmodel import SQLModel, Field, create_engine, Session, select

connection_string = "sqlite:///stdbase.db"
connection = create_engine(connection_string)


class Students(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    phone: str
    address: str | None = None


SQLModel.metadata.create_all(connection)


def add_students(student_list):
    with Session(connection) as session:
        for student in student_list:
            session.add(student)
        session.commit()
    return {"message": "Students added successfully"}


def get_students():
    with Session(connection) as session:
        statement = select(Students)
        results = session.exec(statement)
        students_data = results.all()
    return students_data
