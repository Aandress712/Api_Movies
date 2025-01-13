from models.movie import Movie as MovieModel
from pydantic import BaseModel, Field
from typing import Optional, List

class Movie(BaseModel):  # Este es el modelo de la pelicula
    
    id : Optional[int] =None  # |None = None dice que ese parametro es opcional es otra forma de hacerlo
    title : str = Field( max_length=15, min_length=5)
    overview : str = Field( max_length=100, min_length=15)
    year : int = Field(le=2024)
    rating : float = Field(ge= 1, le=10)
    category : str = Field( max_length=20, min_length=5)

    class Config:
        json_schema_extra = {
            "example": {

                "id" : 1,
                "title" : "Mi Pelicula",
                "overview" : "Descripción de la pelicula",
                "year" : 2022,
                "rating" : 9.8,
                "category" : "Accion"
            }
        }