from fastapi.testclient import TestClient
from app.main import aplicacao

cliente_teste = TestClient(aplicacao)


def test_verificar_saude():
    resposta = cliente_teste.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_buscar_item():
    resposta = cliente_teste.get("/itens/123")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id_item"] == 123
    assert "descricao" in corpo


def test_criar_listar_e_buscar_pedido():
    payload = {
        "nome_cliente": "Felipe",
        "itens": ["mouse", "teclado"],
        "valor_total": 299.9,
    }
    criar = cliente_teste.post("/pedidos", json=payload)
    assert criar.status_code == 201
    pedido = criar.json()
    assert "id_pedido" in pedido
    assert pedido["status"] == "criado"

    listar = cliente_teste.get("/pedidos")
    assert listar.status_code == 200
    assert isinstance(listar.json(), list)
    assert len(listar.json()) >= 1

    buscar = cliente_teste.get(f"/pedidos/{pedido['id_pedido']}")
    assert buscar.status_code == 200
    assert buscar.json()["nome_cliente"] == "Felipe"


def test_buscar_pedido_inexistente_retorna_404():
    resposta = cliente_teste.get("/pedidos/id-inexistente")
    assert resposta.status_code == 404


def test_validacao_payload_invalido_retorna_422():
    payload_invalido = {
        "nome_cliente": "",
        "itens": [],
        "valor_total": -10,
    }
    resposta = cliente_teste.post("/pedidos", json=payload_invalido)
    assert resposta.status_code == 422
