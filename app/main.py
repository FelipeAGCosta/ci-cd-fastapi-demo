# ruff: noqa: B008
from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import obter_db
from app.models import Pedido as PedidoDB
from app.models import PedidoItem as PedidoItemDB

aplicacao = FastAPI(title="API Demonstração CI/CD")


# -----------------------------
# Schemas (Pydantic)
# -----------------------------
class PedidoEntrada(BaseModel):
    nome_cliente: str = Field(min_length=1, max_length=80)
    itens: List[str] = Field(min_length=1, description="Lista de itens do pedido")
    valor_total: float = Field(gt=0, description="Valor total do pedido")


class PedidoSaida(PedidoEntrada):
    id_pedido: str
    status: str = Field(default="criado")


class AtualizacaoStatus(BaseModel):
    status: str = Field(min_length=1, max_length=30)


# -----------------------------
# Helpers
# -----------------------------
def _pedido_db_para_saida(pedido: PedidoDB) -> PedidoSaida:
    return PedidoSaida(
        id_pedido=pedido.id_pedido,
        nome_cliente=pedido.nome_cliente,
        itens=[i.descricao for i in (pedido.itens or [])],
        valor_total=pedido.valor_total,
        status=pedido.status,
    )


# -----------------------------
# Endpoints básicos
# -----------------------------
@aplicacao.get("/saude")
def verificar_saude() -> Dict[str, str]:
    return {"status": "ok"}


@aplicacao.get("/itens/{id_item}")
def buscar_item(id_item: int) -> Dict[str, str | int]:
    return {"id_item": id_item, "descricao": f"Item número {id_item}"}


@aplicacao.get("/")
def raiz():
    return RedirectResponse(url="/docs")


# -----------------------------
# Endpoints (Pedidos) com DB
# -----------------------------
@aplicacao.post("/pedidos", response_model=PedidoSaida, status_code=201)
def criar_pedido(pedido_entrada: PedidoEntrada, db: Session = Depends(obter_db)):
    id_pedido = str(uuid4())

    pedido_db = PedidoDB(
        id_pedido=id_pedido,
        nome_cliente=pedido_entrada.nome_cliente,
        valor_total=pedido_entrada.valor_total,
        status="criado",
    )
    pedido_db.itens = [PedidoItemDB(descricao=texto) for texto in pedido_entrada.itens]

    db.add(pedido_db)
    db.commit()
    db.refresh(pedido_db)

    return _pedido_db_para_saida(pedido_db)


@aplicacao.get("/pedidos", response_model=List[PedidoSaida])
def listar_pedidos(db: Session = Depends(obter_db)):
    stmt = select(PedidoDB).options(selectinload(PedidoDB.itens))
    pedidos = db.execute(stmt).scalars().all()
    return [_pedido_db_para_saida(p) for p in pedidos]


@aplicacao.get("/pedidos/{id_pedido}", response_model=PedidoSaida)
def buscar_pedido(id_pedido: str, db: Session = Depends(obter_db)):
    stmt = (
        select(PedidoDB)
        .where(PedidoDB.id_pedido == id_pedido)
        .options(selectinload(PedidoDB.itens))
    )
    pedido = db.execute(stmt).scalars().first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return _pedido_db_para_saida(pedido)


@aplicacao.patch("/pedidos/{id_pedido}/status", response_model=PedidoSaida)
def atualizar_status_pedido(
    id_pedido: str,
    dados: AtualizacaoStatus,
    db: Session = Depends(obter_db),
):
    
    pedido = db.get(PedidoDB, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.status = dados.status
    db.commit()

    stmt = (
        select(PedidoDB)
        .where(PedidoDB.id_pedido == id_pedido)
        .options(selectinload(PedidoDB.itens))
    )
    pedido_atualizado = db.execute(stmt).scalars().first()
    return _pedido_db_para_saida(pedido_atualizado)


@aplicacao.delete("/pedidos/{id_pedido}", status_code=204)
def deletar_pedido(id_pedido: str, db: Session = Depends(obter_db)):
    pedido = db.get(PedidoDB, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db.delete(pedido)
    db.commit()
    return Response(status_code=204)
