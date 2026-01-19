from fastapi.testclient import TestClient
from app.main import aplicacao

cliente_teste = TestClient(aplicacao)


def test_verificar_saude():
    resposta = cliente_teste.get("/saude")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["status"] == "ok"


def test_buscar_item():
    resposta = cliente_teste.get("/itens/123")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id_item"] == 123
    assert "descricao" in corpo
