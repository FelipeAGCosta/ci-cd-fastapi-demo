from __future__ import annotations

from typing import List

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    nome_cliente: Mapped[str] = mapped_column(String(80), nullable=False)
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="criado")

    itens: Mapped[List["PedidoItem"]] = relationship(
        back_populates="pedido",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pedido_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("pedidos.id_pedido", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    descricao: Mapped[str] = mapped_column(String(200), nullable=False)

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
