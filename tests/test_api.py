import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensagem": "Bem-vindo à API de Recomendação de Produtos"
    }


def test_criar_produtos():
    response = client.post(
        "/produtos/",
        json={
            "nome": "Produtos A",
            "categoria": "Categoria 1",
            "tags": ["tag1", "tag2"],
        },
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Produtos A"


def test_listar_produtos():
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_criar_usuarios():
    response = client.post("/usuarios/", params={"nome": "Usuário Teste"})
    assert response.status_code == 200
    usuario_data = response.json()
    assert usuario_data["id"] == 1
    assert usuario_data["nome"] == "Usuário Teste"


def test_listar_usuarios():
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_criar_historico():
    response = client.post("/historico_compras/1", json={"produtos_ids": [1]})
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Histórico de compras atualizado"}


def test_recomendacoes():
    response = client.post(
        "/recomendacoes/1", json={"categorias": ["Categoria 1"], "tags": ["tag1"]}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
