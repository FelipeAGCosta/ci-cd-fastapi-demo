from __future__ import annotations

from enum import Enum
from typing import Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

aplicacao = FastAPI(title="API Demonstração CI/CD")


# -----------------------------
# Modelos (Pydantic)
# -----------------------------
class StatusPedido(str, Enum):
    criado = "criado"
    pago = "pago"
    separado = "separado"
    enviado = "enviado"
    entregue = "entregue"
    cancelado = "cancelado"


class PedidoEntrada(BaseModel):
    nome_cliente: str = Field(min_length=1, max_length=80)
    itens: List[str] = Field(min_length=1, description="Lista de itens do pedido")
    valor_total: float = Field(gt=0, description="Valor total do pedido")


class Pedido(PedidoEntrada):
    id_pedido: str
    status: StatusPedido = Field(default=StatusPedido.criado)


class AtualizacaoStatus(BaseModel):
    status: StatusPedido


# -----------------------------
# "Banco" em memória (demo)
# -----------------------------
_pedidos: Dict[str, Pedido] = {}


# -----------------------------
# UX: raiz redireciona para /docs
# -----------------------------
@aplicacao.get("/", include_in_schema=False)
def raiz():
    return RedirectResponse(url="/docs")


@aplicacao.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Evita log de 404 no navegador
    return {}


# -----------------------------
# Endpoints básicos (saúde e demo simples)
# -----------------------------
@aplicacao.get("/saude")
def verificar_saude():
    return {"status": "ok"}


@aplicacao.get("/itens/{id_item}")
def buscar_item(id_item: int):
    return {"id_item": id_item, "descricao": f"Item número {id_item}"}


# -----------------------------
# Endpoints "caso real" (pedidos)
# -----------------------------
@aplicacao.post("/pedidos", response_model=Pedido, status_code=201)
def criar_pedido(pedido_entrada: PedidoEntrada):
    id_pedido = str(uuid4())
    pedido = Pedido(
        id_pedido=id_pedido,
        nome_cliente=pedido_entrada.nome_cliente,
        itens=pedido_entrada.itens,
        valor_total=pedido_entrada.valor_total,
        status=StatusPedido.criado,
    )
    _pedidos[id_pedido] = pedido
    return pedido


@aplicacao.get("/pedidos", response_model=List[Pedido])
def listar_pedidos():
    return list(_pedidos.values())


@aplicacao.get("/pedidos/{id_pedido}", response_model=Pedido)
def buscar_pedido(id_pedido: str):
    pedido = _pedidos.get(id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@aplicacao.patch("/pedidos/{id_pedido}/status", response_model=Pedido)
def atualizar_status_pedido(id_pedido: str, dados: AtualizacaoStatus):
    pedido = _pedidos.get(id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.status = dados.status
    _pedidos[id_pedido] = pedido
    return pedido


@aplicacao.delete("/pedidos/{id_pedido}", status_code=204)
def deletar_pedido(id_pedido: str):
    if id_pedido not in _pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    del _pedidos[id_pedido]
    return None
