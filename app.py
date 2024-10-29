from pydantic import BaseModel
from typing import List,Dict
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


produtos: List[Produto]                =[]
contador_produto: int          =1


usuarios: List[Usuario]                 =[]

contador_usuario: int          =1


MENSAGEM_HOME: str    ="Bem-vindo à API de Recomendação de Produtos"

# Histórico de compras em memória
historico_de_compras: Dict[int, List[int]]         ={}

# Criando o App
app = FastAPI()

# Iniciando o servidor

@app.get("/")
def home() -> Dict[str, str]:
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}


# Rota para cadastrar produtos

@app.post("/produtos/", response_model=Produto)
def criar_produto(produto: CriarProduto) -> Produto:
    global contador_produto
    novo_produto = Produto(id=contador_produto, **produto.model_dump())
    produtos.append(novo_produto)
    contador_produto += 1
    return novo_produto


# Rota para listar todos os produtos

@app.get("/produtos/", response_model=List[Produto])
def listar_produtos() -> List[Produto]:
    return produtos

# Rota para simular a criação do histórico de compras de um usuário

@app.post("/historico_compras/{usuario_id}")
def adicionar_historico_compras(usuario_id: int, compras: HistoricoCompras) -> Dict[str, str]:
    if usuario_id not in [usuario.id for usuario in usuarios]:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    historico_de_compras[usuario_id] = compras.produtos_ids
    return {"mensagem": "Histórico de compras atualizado"}

# Rota para recomendações de produtos

@app.post("/recomendacoes/{usuario_id}", response_model=List[Produto])
def recomendar_produtos(usuario_id: int, preferencias: Preferencias) -> List[Produto]:
    if usuario_id not in historico_de_compras:
        raise HTTPException(status_code=404, detail="Histórico de compras não encontrado")

    produtos_recomendados = []

    # Buscar produtos com base no histórico de compras do usuário

    produtos_recomendados = [produto for produto_id in historico_de_compras[usuario_id] for produto in produtos if produto.id == produto_id]

    # Filtrar as recomendações com base nas preferências
    produtos_recomendados = [p for p in produtos_recomendados if p.categoria in preferencias.categorias] # Preferencias de categorias
    produtos_recomendados = [p for p in produtos_recomendados if any(tag in preferencias.tags for tag in p.tags)] # Preferencias de tags

    return produtos_recomendados

# Rota para cadastrar usuários

@app.post("/usuarios/", response_model=Usuario)
def criar_usuario(nome: str) -> Usuario:
    global contador_usuario
    novo_usuario = Usuario(id=contador_usuario, nome=nome)
    usuarios.append(novo_usuario)
    contador_usuario += 1
    return novo_usuario

# Rota para listar usuários

@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios() -> List[Usuario]:
    return usuarios