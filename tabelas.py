from database import Base, engine
from sqlalchemy import String,Integer, Column, ForeignKey, Table, Date, Float, DateTime
from sqlalchemy.orm import relationship


following_artists = Table('following_artists', Base.metadata,
    Column('usuarios_id', ForeignKey('usuarios.id'), primary_key=True),
    Column('artistas_id', ForeignKey('artistas.id'), primary_key=True)
)



class Usuarios(Base):
    __tablename__="usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(256), nullable= False, unique = True)
    data_assinatura = Column(Date, nullable=False)
    planos_id  = Column(Integer,ForeignKey('planos.id')) 

    plano = relationship('Planos', back_populates='usuario')
    artista = relationship("Artistas", secondary='following_artists')
    musica = relationship("Musicas", secondary='historico', back_populates='usuario')



class Planos(Base):
    __tablename__="planos"
    id = Column(Integer, primary_key=True)
    nome_plano = Column(String(256), nullable= False, unique = True)
    valor= Column(Float, nullable = False)

    usuario = relationship('Usuarios', back_populates = 'plano')



class Artistas(Base):
    __tablename__="artistas"
    id = Column(Integer, primary_key=True)
    nome = Column(String(256), nullable= False, unique = True)

    #usuarios = relationship("Artistas", secondary='following_artists', back_populates='artista')
    album = relationship('Albuns', back_populates='artista')
    musica = relationship('Musicas', back_populates = 'artista')




class Albuns(Base):
    __tablename__="albuns"
    id = Column(Integer, primary_key=True)
    nome = Column(String(256), nullable= False, unique = True)
    ano = Column(Integer, nullable= False, unique = True)
    artistas_id = Column(Integer,ForeignKey('artistas.id'))

    artista = relationship('Artistas', back_populates='album')
    musica = relationship("Musicas", back_populates = 'album')




class Musicas(Base):
    __tablename__="musicas"
    id = Column(Integer, primary_key=True)
    nome = Column(String(256), nullable= False, unique = True)
    artistas_id = Column(Integer,ForeignKey('artistas.id'))
    album_id = Column(Integer,ForeignKey('albuns.id'))

    artista = relationship("Artistas", back_populates='musica')
    album = relationship("Albuns", back_populates = 'musica')
    usuario = relationship("Usuarios", secondary='historico', back_populates='musica')



class Historico(Base):
    __tablename__= "historico"
    usuario_id = Column(Integer,ForeignKey('usuarios.id'), primary_key=True)
    musica_id = Column(Integer,ForeignKey('musicas.id'), primary_key=True)
    data_reproducao =  Column(DateTime, nullable=False)

    