from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import obter_db
from app.main import aplicacao
from app.models import Base


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def _override_obter_db():
        db: Session = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    aplicacao.dependency_overrides[obter_db] = _override_obter_db

    with TestClient(aplicacao) as c:
        yield c

    aplicacao.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
