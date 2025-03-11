from pydantic import BaseModel, Field # La propiedad Fiel puede limitar las cosas

class User(BaseModel):
    email:str
    password: str