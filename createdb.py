from database import Base, engine
from tabelas import Usuarios,Planos, Artistas, Albuns, Musicas, following_artists, Historico
print("Creating database...")

Base.metadata.create_all(engine)
