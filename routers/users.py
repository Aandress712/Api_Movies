from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from config.database import Session
from models.usuario import User as Usuario
from typing import Optional, List
from pydantic import BaseModel, Field 
from routers.users import APIRouter
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from schemas.user import User

user_api= APIRouter()

@user_api.post('/login', tags=['Auth'])

def login(user: User):

    if user.email=="admin" and user.password=="123":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    if user.email=="andres" and user.password=="712":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    
    return JSONResponse(status_code=404, content="Auth Failed")

@user_api.post('/user', tags =['Auth'])

def create_user(user : User) -> dict:  # Esta hace lo mismo de la de arriba pero con el modelo que le indicamos
    db = Session()
    new_user = Usuario(**user.dict())
    db.add(new_user)
    db.commit()
    return JSONResponse (content={"message": "Se Registro la pelicula"}, status_code=201)

@user_api.get("/Usuarios", tags= ["Auth"], status_code=200, dependencies=[Depends(JWTBearer())])

def get_movies() -> List [User]:                   # Con -> List digo que la funcion va a retornar una lista
    
    db = Session()
    result = db.query(Usuario).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)