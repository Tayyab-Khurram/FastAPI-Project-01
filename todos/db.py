from sqlmodel import SQLModel, Field, create_engine

connection_string = "sqlite:///stdbase.db"
connection = create_engine(connection_string)


class Students(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    address: str
    phone: int


SQLModel.metadata.create_all(connection)
