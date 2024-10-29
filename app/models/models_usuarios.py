from pydantic import BaseModel


# Modelo base para um usuário
class Usuario(BaseModel):
    id: int
    nome: str
