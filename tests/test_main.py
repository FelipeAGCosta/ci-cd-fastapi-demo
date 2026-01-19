from fastapi.testclient import TestClient

from app.main import aplicacao

cliente = TestClient(aplicacao)


def test_verificar_saude():
    resposta = cliente.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_raiz_redireciona_para_docs():
    # O TestClient segue redirect por padrão, então checamos o final
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "/docs" in str(resposta.url)


def test_crud_pedidos_fluxo_basico():
    # 1) Criar pedido
    payload = {
        "nome_cliente": "Felipe",
        "itens": ["mouse", "teclado"],
        "valor_total": 199.90,
    }
    resp_criar = cliente.post("/pedidos", json=payload)
    assert resp_criar.status_code == 201
    pedido_criado = resp_criar.json()
    assert "id_pedido" in pedido_criado
    assert pedido_criado["nome_cliente"] == "Felipe"
    assert pedido_criado["status"] == "criado"

    id_pedido = pedido_criado["id_pedido"]

    # 2) Buscar pedido
    resp_buscar = cliente.get(f"/pedidos/{id_pedido}")
    assert resp_buscar.status_code == 200
    assert resp_buscar.json()["id_pedido"] == id_pedido

    # 3) Listar pedidos
    resp_listar = cliente.get("/pedidos")
    assert resp_listar.status_code == 200
    lista = resp_listar.json()
    assert isinstance(lista, list)
    assert any(p["id_pedido"] == id_pedido for p in lista)

    # 4) Atualizar status
    resp_status = cliente.patch(f"/pedidos/{id_pedido}/status", json={"status": "enviado"})
    assert resp_status.status_code == 200
    assert resp_status.json()["status"] == "enviado"

    # 5) Deletar pedido
    resp_deletar = cliente.delete(f"/pedidos/{id_pedido}")
    assert resp_deletar.status_code == 204

    # 6) Garantir que não existe mais
    resp_buscar_depois = cliente.get(f"/pedidos/{id_pedido}")
    assert resp_buscar_depois.status_code == 404
