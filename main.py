from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
import tabelas
from classes import ArtistasOut, Usuarios, UsuariosOut, Planos, Artistas, Albuns,AlbunsOut,Musicas,MusicasOut,Albuns_Out
from typing import List
from database import SessionLocal
from sqlalchemy.orm import joinedload
from fastapi.templating import Jinja2Templates 
import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db = SessionLocal()



#Você receberá uma resposta informando que os dados são inválidos contendo o corpo recebido
@app.exception_handler(RequestValidationError)
async def validation_error(request:Request,exc:RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail":exc.errors(),"body":exc.body})
    )
        
    

@app.get("/")
async def hello(request:Request):
    """
    **Boas vindas**
    """

    ola=str("Seja bem-vindo ao music sound!")
    print("\n"+str(ola)+"\n")
    return templates.TemplateResponse("index.html",{"request":request,"ola":ola})


@app.get("/planos/", response_model=List[Planos],status_code=status.HTTP_200_OK)
async def lista_planos():
    planos = db.query(tabelas.Planos).all()

    if planos == None:
        print("\nNenhum plano encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum plano encontrado")

    return planos

@app.get("/planos/{id}", response_model=Planos, status_code=status.HTTP_200_OK)
async def busca_planos(id:int):
    """
    Função que realiza a busca de um determinado aluno através de seu **Id**
    """
         
    plano = db.query(tabelas.Planos).filter(tabelas.Planos.id==id).first() #busca pelo ID

    if plano == None:
        print("\nPlano não encontrado\n")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Plano não encontrado')
     
    return plano

@app.post("/planos/", response_model=Planos, status_code=status.HTTP_201_CREATED)
async def new_plan(plano: Planos):
    """
    Cria um novo plano
    
    - **id**: 
    - **nome**: 
    
    """

    novo_plano=tabelas.Planos(nome_plano = plano.nome_plano)
    db.add(novo_plano)
    db.commit()
    
    print("\nid: "+str(novo_plano.id))
    print("nome: "+str(novo_plano.nome_plano))
   
    print("\Plano cadastrado com sucesso\n")

    return novo_plano


@app.get("/usuarios/", response_model=List[UsuariosOut],status_code=status.HTTP_200_OK)
async def lista_usuarios():
    usuario = db.query(tabelas.Usuarios).options(joinedload(tabelas.Usuarios.plano)).all()

    if usuario == None:
        print("\nNenhum usuário encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum usuário encontrado")

    total="Total de usuários cadastrados: "+str(len(usuario))
   
    print("\n"+str(total)+"\n")

    return usuario


@app.get("/usuarios/{id}", response_model=UsuariosOut, status_code=status.HTTP_200_OK)
async def busca_usuario(id:int):
    """
    Função que realiza a busca de um determinado aluno através de seu **Id**
    """
         
    user = db.query(tabelas.Usuarios).filter(tabelas.Usuarios.id==id).first() #busca pelo ID

    if user == None:
        print("\nUsuário não encontrado\n")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Usuário não encontrado')
     
    return user

@app.post("/usuarios/", response_model=Usuarios, status_code=status.HTTP_201_CREATED)
async def new_user(usuario: Usuarios):
    """
    Cria um novo usuário
    
    - **id**: 
    - **nome**: 
    
    """
    
    data_atual = datetime.date.today()

    novo_usuario=tabelas.Usuarios(nome = usuario.nome,data_assinatura=data_atual, planos_id = usuario.planos_id)
    db.add(novo_usuario)
    db.commit()
    
    print("\nid: "+str(novo_usuario.id))
    print("nome: "+str(novo_usuario.nome))
    print("nome: "+str(novo_usuario.data_assinatura))
   
    print("\nUsuário cadastrado com sucesso\n")

    return novo_usuario


@app.get("/artistas/", response_model=List[Artistas],status_code=status.HTTP_200_OK)
async def lista_artistas():
    artista = db.query(tabelas.Artistas).all()

    if artista == None:
        print("\nNenhum registro encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum registro encontrado")

    total="Total de artistas cadastrados: "+str(len(artista))
   
    print("\n"+str(total)+"\n")

    return artista


@app.get("/artistas/{id}", response_model=Artistas, status_code=status.HTTP_200_OK)
async def busca_artista(id:int):
    """
    Função que realiza a busca de um determinado artista através de seu **Id**
    """
         
    artista = db.query(tabelas.Artistas).filter(tabelas.Artistas.id==id).first() #busca pelo ID

    if artista == None:
        print("\nNenhum artista encontrado\n")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Nenhum artista encontrado')
     
    return artista




@app.post("/artistas/", response_model=Artistas, status_code=status.HTTP_201_CREATED)
async def new_artista(artista: Artistas):
    """
    Cria um novo artista
    
    - **id**: 
    - **nome**: 
    
    """
    
    
    novo_artista=tabelas.Artistas(nome = artista.nome)
    db.add(novo_artista)
    db.commit()
    
    print("\nid: "+str(novo_artista.id))
    print("nome: "+str(novo_artista.nome))
    
   
    print("\nArtista cadastrado com sucesso\n")

    return novo_artista



@app.get("/albuns/", response_model=List[AlbunsOut],status_code=status.HTTP_200_OK)
async def lista_albuns():
    album = db.query(tabelas.Albuns).options(joinedload(tabelas.Albuns.artista)).all()

    if album == None:
        print("\nNenhum álbum encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum álbum encontrado")

    total="Total de álbuns cadastrados: "+str(len(album))
   
    print("\n"+str(total)+"\n")

    return album


@app.get("/albuns/{id}", response_model=Albuns_Out, status_code=status.HTTP_200_OK)
async def busca_album(id:int):
    """
    Função que realiza a busca de um determinado álbum através de seu **Id**
    """
         
    album = db.query(tabelas.Albuns).filter(tabelas.Albuns.id==id).first() #busca pelo ID

    if album == None:
        print("\nÁlbum não encontrado\n")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Álbum não encontrado')
     
    return album


@app.post("/albuns/", response_model=Albuns, status_code=status.HTTP_201_CREATED)
async def new_album(albuns: Albuns):
    """
    Cria um novo álbum
    
    - **id**: 
    - **nome**: 
    - **ano**:
    
    """
    
    
    novo_album=tabelas.Albuns(nome = albuns.nome, ano = albuns.ano,artistas_id=albuns.artistas_id)
    db.add(novo_album)
    db.commit()
    
    print("\nid: "+str(novo_album.id))
    print("nome: "+str(novo_album.nome))
    print("ano de lançamento: "+str(novo_album.ano))
   
    print("\nÁlbum cadastrado com sucesso\n")

    return novo_album



@app.get("/musicas/", response_model=List[MusicasOut],status_code=status.HTTP_200_OK)
async def lista_musicas():
    musica = db.query(tabelas.Musicas).options(joinedload(tabelas.Musicas.album)).all()

    if musica == None:
        print("\nErro! Nenhuma música encontrada.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro! Nenhuma música encontrada.")

    total="Total de músicas cadastradas: "+str(len(musica))
   
    print("\n"+str(total)+"\n")

    return musica


@app.get("/musicas/{id}", response_model=MusicasOut, status_code=status.HTTP_200_OK)
async def busca_musica(id:int):
    """
    Função que realiza a busca de uma determinada música através de seu **Id**
    """
         
    musica = db.query(tabelas.Musicas).filter(tabelas.Musicas.id==id).first() #busca pelo ID

    if musica == None:
        print("\nErro! Nenhuma música encontrada.\n")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Erro! Nenhuma música encontrada.')
     
    return musica


@app.post("/musicas/", response_model=Musicas, status_code=status.HTTP_201_CREATED)
async def new_music(musica: Musicas):
    """
    Cria uma nova música
   
    
    """
    
    
    nova_musica=tabelas.Musicas(nome = musica.nome,artistas_id = musica.artistas_id,album_id=musica.album_id)
    db.add(nova_musica)
    db.commit()
    
    print("\nid: "+str(nova_musica.id))
    print("nome: "+str(nova_musica.nome))
    
   
    print("\nMúsica cadastrada com sucesso\n")

    return nova_musica