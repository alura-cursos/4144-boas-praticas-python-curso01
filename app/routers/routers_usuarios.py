from typing import List
from fastapi import APIRouter
from app.models.models_usuarios import Usuario

router = APIRouter()


usuarios: List[Usuario] = []

contador_usuario: int = 1



@router.post("/usuarios/", response_model=Usuario)
def criar_usuario(nome: str) -> Usuario:
    """
    Cria um novo usuário.

    Args:
        nome (str): O nome do usuário a ser criado.

    Returns:
        Usuario: O objeto do usuário recém-criado com um ID gerado.
    """
    global contador_usuario
    novo_usuario = Usuario(id=contador_usuario, nome=nome)
    usuarios.append(novo_usuario)
    contador_usuario += 1
    return novo_usuario


# Rota para listar usuários


@router.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios() -> List[Usuario]:
    """
    Lista todos os usuários cadastrados.

    Returns:
        List[Usuario]: Uma lista de objetos de usuários cadastrados.
    """
    return usuarios
