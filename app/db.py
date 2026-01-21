from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def normalizar_url_banco(url: str) -> str:
    """
    Render costuma fornecer postgresql://...
    Para psycopg3 + SQLAlchemy, preferimos postgresql+psycopg://...
    """
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = normalizar_url_banco(os.getenv("DATABASE_URL", "sqlite:///./app.db"))

_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=_connect_args,
)

SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def obter_db() -> Generator[Session, None, None]:
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()
