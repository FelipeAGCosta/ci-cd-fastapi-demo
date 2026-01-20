from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "0001_cria_tabelas_pedidos"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pedidos",
        sa.Column("id_pedido", sa.String(length=36), primary_key=True),
        sa.Column("nome_cliente", sa.String(length=80), nullable=False),
        sa.Column("valor_total", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="criado"),
    )
    op.create_index("ix_pedidos_id_pedido", "pedidos", ["id_pedido"])

    op.create_table(
        "pedido_itens",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("pedido_id", sa.String(length=36), nullable=False),
        sa.Column("descricao", sa.String(length=200), nullable=False),
        sa.ForeignKeyConstraint(
            ["pedido_id"],
            ["pedidos.id_pedido"],
            ondelete="CASCADE",
        ),
    )
    op.create_index("ix_pedido_itens_pedido_id", "pedido_itens", ["pedido_id"])


def downgrade() -> None:
    op.drop_index("ix_pedido_itens_pedido_id", table_name="pedido_itens")
    op.drop_table("pedido_itens")

    op.drop_index("ix_pedidos_id_pedido", table_name="pedidos")
    op.drop_table("pedidos")
