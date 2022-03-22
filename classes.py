from datetime import date
from pydantic import BaseModel, ValidationError
from typing import List 


class Usuarios(BaseModel):
    id:int
    nome: str
    data_assinatura: date
    planos_id: int

    class Config:
        orm_mode= True

class Planos(BaseModel):
    id:int
    nome_plano:str
    valor:float

    class Config:
        orm_mode = True


class UsuariosOut(BaseModel):
    id:int
    nome: str
    data_assinatura: date
    plano:Planos

    class Config:
        orm_mode= True


class Artistas(BaseModel):
    id: int
    nome: str
    
    class Config:
        orm_mode= True


class Albuns(BaseModel):
    id: int
    nome: str
    ano: int
    artistas_id:int

    class Config:
        orm_mode= True


class AlbunSchema(BaseModel):
    nome:str
    ano: int

    class Config:
        orm_mode=True



class ArtistasOut(BaseModel):
    nome: str
   
    class Config:
        orm_mode= True


class Musicas(BaseModel):
    id: int 
    nome: str
    artistas_id: int
    album_id: int


    class Config:
        orm_mode= True

class MusicaSchema(BaseModel):
    
    nome:str

    class Config:
        orm_mode = True

class MusicasOut(BaseModel):
    id: int 
    nome: str
    album: AlbunSchema
    artista: ArtistasOut


    class Config:
        orm_mode= True


class AlbunsOut(BaseModel):
    id: int
    nome: str
    ano: int
    artista: ArtistasOut
    

    class Config:
        orm_mode= True 

class Albuns_Out(BaseModel):
    id: int
    nome: str
    ano: int
    artista: ArtistasOut
    musica: List[MusicaSchema]

    class Config:
        orm_mode= True 