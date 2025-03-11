from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel               # La propiedad Fiel puede limitar las cosas
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler #-> Clase donde esta la exepcion
from routers.movie import movie_router
from routers.users import user_api

app = FastAPI()
app.title = "My First Application with FAST API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler) #-> Manejo de Errors de la app
app.include_router(user_api)
app.include_router(movie_router)

Base.metadata.create_all(bind = engine)


movies = [
    {
    "id" : 1,
    "title" : "Avatar",
    "overview" : "En un Exuberantes Planeta llamda Pandora viven los Na'vies",
    "year" : "2009",
    "rating" : 7.8,
    "category" : "Accion"
    },
    {
    "id" : 2,
    "title" : "Terminator",
    "overview" : "Un Robot llega del pasado para salvar la humanidad",
    "year" : "1985",
    "rating" : 8.8,
    "category" : "Ficción"
    }
]

@app.get('/', tags= ["Home"])

def message():
    return HTMLResponse ("<h1>Hello World muy pleno</h1>")


#--------------------------------------------------------------------------------------------------------------

#  Esto ya no es necesario por los routers de Fast API APIRouter


#  
#  class User(BaseModel):
#      email:str
#      password: str
#  
#  @app.post('/login', tags=['auth'])
#  
#  def login(user: User):
#      if user.email=="admin" and user.password=="123":
#          token: str = create_token(user.dict())
#          return JSONResponse(status_code=200, content=token)
#      
#      return JSONResponse(status_code=404, content="Auth Failed")
#  
#  class Movie(BaseModel):  # Este es el modelo de la pelicula
#      
#      id : Optional[int] =None  # |None = None dice que ese parametro es opcional es otra forma de hacerlo
#      title : str = Field( max_length=15, min_length=5)
#      overview : str = Field( max_length=100, min_length=15)
#      year : int = Field(le=2024)
#      rating : float = Field(ge= 1, le=10)
#      category : str = Field( max_length=20, min_length=5)
#  
#      class Config:
#          json_schema_extra = {
#              "example": {
#  
#                  "id" : 1,
#                  "title" : "Mi Pelicula",
#                  "overview" : "Descripción de la pelicula",
#                  "year" : 2022,
#                  "rating" : 9.8,
#                  "category" : "Accion"
#              }
#          }
#  
#  
#  @app.get("/Movies", tags= ["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
#  
#  def get_movies() -> List [Movie]:                   # Con -> List digo que la funcion va a retornar una lista
#      
#      db = Session()
#      result = db.query(MovieModel).all()
#      return JSONResponse(content=jsonable_encoder(result), status_code=200)
#  
#  
#  @app.get('/Movies/{id}', tags= ["Movies"], response_model=Movie)  # el ID es un parametro obligatorio y busca en un diccionario de movies
#  
#  def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
#  
#      db = Session()
#      result = db.query(MovieModel).filter(MovieModel.id == id).first()
#      if not result:
#          return JSONResponse(status_code=404, content={'message' : "Id Pelicula no encontrado"})
#      return JSONResponse(status_code=200, content=jsonable_encoder(result))
#      
#  #    for item in movies:
#  #        if item["id"] == id:
#  #            return JSONResponse(content=item)
#  #    return JSONResponse(status_code=404, content="El Id de la pelicula no existe")
#  
#  @app.get('/Movies/{category}', tags= ["Movies"], response_model=List[Movie])  # el ID es un parametro query y busca en un diccionario de movies
#  
#  def get_movie(category: str) -> List[Movie]:
#  
#      db = Session()
#      result = db.query(MovieModel).filter(MovieModel.category == category).all()
#      if not result:
#          return JSONResponse(status_code=404, content={'message' : "No contamos con la categoria suministrada"})
#      return JSONResponse(status_code=200, content=jsonable_encoder(result))
#  
#  #    peliculas = []         Otra solución
#  #    for item in movies:
#  #        if item["category"] in category:
#  #            peliculas.append(item)
#  #    return peliculas
#  
#  #    data = [item for item in movies if item ["category"] in category]
#  #    return JSONResponse(content=data)
#  
#  @app.post('/movies', tags =["Movies"], response_model=dict, status_code=201)
#  
#  #def create_movie(id = Body(), title= Body(), overview= Body(), year= Body(), rating= Body(), category= Body()):
#  #    movies.append(
#  #        {
#  #        "id" : id,
#  #        "title" : title,
#  #        "overview" : overview,
#  #        "year" : year,
#  #        "rating" : rating,
#  #        "category" : category
#  #        })
#  #        return movies
#  def create_movie (movie : Movie) -> dict:  # Esta hace lo mismo de la de arriba pero con el modelo que le indicamos
#      db = Session()
#      new_movie = MovieModel(**movie.dict())
#      db.add(new_movie)
#      db.commit()
#  #    movies.append(movie)
#      return JSONResponse (content={"message": "Se Registro la pelicula"}, status_code=201)
#  
#  @app.put('/Movies/{id}', tags= ["Movies"], response_model=dict, status_code=200)
#  
#  def update_movie(id: int, movie:Movie)-> dict:
#  
#      db = Session()
#      result = db.query(MovieModel).filter(MovieModel.id == id).first()
#      if not result:
#          return JSONResponse(status_code= 404, content={'message':"No existe ninguna pelicula con este id: f.id"})
#      result.title = movie.title
#      result.year = movie.year
#      result.overview = movie.overview
#      result.category = movie.category
#      result.rating = movie.rating 
#      db.commit()
#      return JSONResponse (status_code= 200, content={'message':"Modificación realizada correctamente"})
#  
#  #def update_movie(id: int, title= Body(), overview= Body(), year= Body(), rating= Body(), category= Body())-> dict:
#  #    for item in movies:
#  #        if item["id"] == id:
#  #            item ['title'] = title,
#  #            item ['overview'] = overview,
#  #            item ['year'] = year,
#  #            item ['rating'] = rating,
#  #            item ['category'] = category
#  #            return JSONResponse (content={"message": "Se Atualizo la pelicula"}, status_code=200)
#  
#  @app.delete('/Movies/{id}', tags= ["Movies"], response_model=dict, status_code=200)
#  
#  def delete_movie(id: int) -> dict:
#      
#      db = Session()
#      result = db.query(MovieModel).filter(MovieModel.id == id).first()
#      if not result:
#          return JSONResponse(status_code= 404, content= {'message':"No de encontro una pelicula con el id proporcionado"})
#      db.delete(result)
#      db.commit()
#      return JSONResponse (content={"message": "Se Elimino la pelicula"}, status_code=200)
#          
#  
#  
#  #@app.delete('/Movies/{id}', tags= ["Movies"], response_model=dict, status_code=200)
#  #
#  #def delete_movie(id: int) -> dict:
#  #    
#  #    for item in movies:
#  #        if item["id"] == id:
#  #            movies.remove(item)
#  #
#  #            return JSONResponse (content={"message": "Se Elimino la pelicula"}, status_code=200)
#  
#  