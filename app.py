from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException




# Modelo base para produto
class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    tags: List[str]


# Modelo para criar um produto
class CriarProduto(ProdutoBase):
    pass

# Modelo de produto com ID
class Produto(ProdutoBase):
    id: int


# Modelo para histórico de compras do usuário
class HistoricoCompras(BaseModel):
    produtos_ids: List[int]


# Modelo para preferências do usuário
class Preferencias(BaseModel):
    categorias: List[str] | None = None
    tags: List[str] | None = None


# Modelo base para um usuário
class Usuario(BaseModel):
    id: int
    nome: str


Produtos                 =[]
ContadorProduto          =1


Usuarios                 =[]

ContadorUsuario          =1


ConstanteMensagemHome    ="Bem-vindo à API de Recomendação de Produtos"

# Histórico de compras em memória
HistoricoDeCompras         ={}

# Criando o App
app = FastAPI()

# Iniciando o servidor

@app.get("/")
def home():
    global ConstanteMensagemHome
    return {"mensagem": ConstanteMensagemHome}


# Rota para cadastrar produtos

@app.post("/produtos/", response_model=Produto)
def criarproduto(produto: CriarProduto):
    global ContadorProduto
    NovoProduto = Produto(id=ContadorProduto, **produto.model_dump())
    Produtos.append(NovoProduto)
    ContadorProduto += 1
    return NovoProduto


# Rota para listar todos os produtos

@app.get("/produtos/", response_model=List[Produto])
def listarprodutos():
    return Produtos

# Rota para simular a criação do histórico de compras de um usuário

@app.post("/historico_compras/{usuario_id}")
def adicionarhistoricocompras(usuario_id: int, compras: HistoricoCompras):
    if usuario_id not in [usuario.id for usuario in Usuarios]:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    HistoricoDeCompras[usuario_id] = compras.produtos_ids
    return {"mensagem": "Histórico de compras atualizado"}

# Rota para recomendações de produtos

@app.post("/recomendacoes/{usuario_id}", response_model=List[Produto])
def recomendarprodutos(usuario_id: int, preferencias: Preferencias):
    if usuario_id not in HistoricoDeCompras:
        raise HTTPException(status_code=404, detail="Histórico de compras não encontrado")

    produtos_recomendados = []

    # Buscar produtos com base no histórico de compras do usuário

    produtos_recomendados = [produto for produto_id in HistoricoDeCompras[usuario_id] for produto in Produtos if produto.id == produto_id]

    # Filtrar as recomendações com base nas preferências
    produtos_recomendados = [p for p in produtos_recomendados if p.categoria in preferencias.categorias] # Preferencias de categorias
    produtos_recomendados = [p for p in produtos_recomendados if any(tag in preferencias.tags for tag in p.tags)] # Preferencias de tags

    return produtos_recomendados

# Rota para cadastrar usuários

@app.post("/usuarios/", response_model=Usuario)
def criarusuario(nome: str):
    global ContadorUsuario
    NovoUsuario = Usuario(id=ContadorUsuario, nome=nome)
    Usuarios.append(NovoUsuario)
    ContadorUsuario += 1
    return NovoUsuario

# Rota para listar usuários

@app.get("/usuarios/", response_model=List[Usuario])
def listarusuarios():
    return Usuarios