from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field               # La propiedad Fiel puede limitar las cosas
from typing import Optional, List                   # Con Optional defino que atributos puedes ser opcionales en el modelo
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from routers.movie import APIRouter
from services.movie import MovieService
from schemas.movie import Movie


movie_router = APIRouter()


@movie_router.get("/Movies", tags= ["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])

def get_movies() -> List [Movie]:                   # Con -> List digo que la funcion va a retornar una lista
    
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/Movies/{id}', tags= ["Movies"], response_model=Movie)  # el ID es un parametro obligatorio y busca en un diccionario de movies

def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:

    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message' : "Id Pelicula no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    
#@movie_router.get('/movies/', tags= ['movies'], response_model=List[Movie])  # el ID es un parametro query y busca en un diccionario de movies

def get_movie_by_cat(category: str = Query(min_length=5, max_digits=15)) -> List[Movie]:

    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    #if not result:
    #    return JSONResponse(status_code=404, content={'message' : "No contamos con la categoria suministrada"})
    

@movie_router.post('/movies', tags =["Movies"], response_model=dict, status_code=201)

def create_movie (movie : Movie) -> dict:  # Esta hace lo mismo de la de arriba pero con el modelo que le indicamos
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse (content={"message": "Se Registro la pelicula"}, status_code=201)


@movie_router.put('/Movies/{id}', tags= ["Movies"], response_model=dict, status_code=200)

def update_movie(id: int, movie:Movie)-> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code= 404, content={'message':"No existe ninguna pelicula con este id: f.id"})
    result.title = movie.title
    result.year = movie.year
    result.overview = movie.overview
    result.category = movie.category
    result.rating = movie.rating 
    db.commit()
    return JSONResponse (status_code= 200, content={'message':"Modificación realizada correctamente"})


@movie_router.delete('/Movies/{id}', tags= ["Movies"], response_model=dict, status_code=200)

def delete_movie(id: int) -> dict:
    
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code= 404, content= {'message':"No de encontro una pelicula con el id proporcionado"})
    db.delete(result)
    db.commit()
    return JSONResponse (content={"message": "Se Elimino la pelicula"}, status_code=200)
      