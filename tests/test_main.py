def test_saude(client):
    r = client.get("/saude")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_criar_listar_e_buscar_pedido(client):
    payload = {"nome_cliente": "Felipe", "itens": ["abc", "xyz"], "valor_total": 10.5}
    r = client.post("/pedidos", json=payload)
    assert r.status_code == 201
    criado = r.json()
    assert criado["nome_cliente"] == "Felipe"
    assert criado["itens"] == ["abc", "xyz"]

    r = client.get("/pedidos")
    assert r.status_code == 200
    lista = r.json()
    assert len(lista) == 1

    r = client.get(f"/pedidos/{criado['id_pedido']}")
    assert r.status_code == 200
    assert r.json()["id_pedido"] == criado["id_pedido"]


def test_atualizar_status_e_deletar(client):
    payload = {"nome_cliente": "Teste", "itens": ["item"], "valor_total": 1}
    r = client.post("/pedidos", json=payload)
    criado = r.json()
    pid = criado["id_pedido"]

    r = client.patch(f"/pedidos/{pid}/status", json={"status": "pago"})
    assert r.status_code == 200
    assert r.json()["status"] == "pago"

    r = client.delete(f"/pedidos/{pid}")
    assert r.status_code == 204

    r = client.get(f"/pedidos/{pid}")
    assert r.status_code == 404
