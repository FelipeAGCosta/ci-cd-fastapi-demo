![CI](https://github.com/FelipeAGCosta/ci-cd-fastapi-demo/actions/workflows/ci.yml/badge.svg)

# API CI/CD com FastAPI, Docker e GitHub Actions

API REST em **Python (FastAPI)** com **testes automatizados (pytest)**, **lint e quality gate (ruff + coverage)**, containerizada com **Docker** e validada automaticamente via **GitHub Actions** a cada push/PR na branch `main`.  
Além disso, a aplicação está publicada em produção (**Render**) com **PostgreSQL** e **migrations (Alembic)**.

## 🔗 Links
- **Produção (raiz)**: https://ci-cd-fastapi-demo-zl88.onrender.com (redireciona para `/docs`)
- **Swagger (/docs)**: https://ci-cd-fastapi-demo-zl88.onrender.com/docs
- **Healthcheck (/saude)**: https://ci-cd-fastapi-demo-zl88.onrender.com/saude
- **Docker Hub**: `felipeagcosta/ci-cd-fastapi-demo`

## ✅ O que este projeto demonstra
- Criação de API REST com FastAPI
- Testes automatizados com `pytest`
- Cobertura de testes com `pytest-cov` (quality gate)
- Lint/boas práticas com `ruff`
- Containerização com Docker (Dockerfile)
- CI no GitHub Actions (lint + testes + coverage + build da imagem)
- Publicação de imagem no Docker Hub (tag `latest` + tag por commit)
- Deploy em produção no Render (build via Dockerfile)
- Banco PostgreSQL + migrations com Alembic (padrão de projeto real)

## 📸 Evidências (CI/CD e Deploy)

### ✅ GitHub Actions (pipeline verde)
<img src="docs/img/actions-sucesso.png" alt="GitHub Actions - pipeline verde" width="560">

### 🐳 Docker Hub (tags `latest` + SHA do commit)
<img src="docs/img/dockerhub-tags.png" alt="Docker Hub - tags" width="560">

### 🌐 Render (serviço em produção / Live)
<img src="docs/img/render-live.png" alt="Render - live" width="560">

### 📚 Swagger (endpoints disponíveis)
<img src="docs/img/swagger-endpoints.png" alt="Swagger - endpoints" width="560">

## 🚀 Endpoints principais
- `GET /` → redireciona para `/docs`
- `GET /saude` → verifica se a API está respondendo
- `GET /docs` → documentação Swagger
- `POST /pedidos` → cria pedido
- `GET /pedidos` → lista pedidos
- `GET /pedidos/{id_pedido}` → busca pedido
- `PATCH /pedidos/{id_pedido}/status` → atualiza status do pedido
- `DELETE /pedidos/{id_pedido}` → deleta pedido

## ▶️ Rodar local (sem Docker)
> Recomendado para desenvolvimento.

```bash
pip install -r requirements.txt
ruff check .
pytest --cov=app --cov-report=term-missing
uvicorn app.main:aplicacao --reload --port 8003
```

Acesse:

http://127.0.0.1:8003/saude

http://127.0.0.1:8003/docs

## 🐳 Rodar com Docker (build local)
```bash
docker build -t ci-cd-fastapi-demo:dev .
docker run --rm -p 8003:8000 ci-cd-fastapi-demo:dev
```
Acesse:

http://localhost:8003/saude

http://localhost:8003/docs

### Por que -p 8003:8000?
Dentro do container a API roda na porta 8000 (padrão).
No seu PC você acessa pela 8003.
Isso mapeia 8003 (host) → 8000 (container).

Se a porta 8003 estiver ocupada:
```bash
docker run --rm -p 8004:8000 ci-cd-fastapi-demo:dev
``` 

## 📦 Rodar a imagem do Docker Hub (sem build)
```bash 
docker pull felipeagcosta/ci-cd-fastapi-demo:latest
docker run --rm -p 8003:8000 felipeagcosta/ci-cd-fastapi-demo:latest
```

## 🗄️ Banco de dados (PostgreSQL + Alembic)
A aplicação usa a variável de ambiente DATABASE_URL.

- Local: você pode apontar para SQLite ou Postgres.

- Produção (Render): a aplicação roda com PostgreSQL.

## Rodar migrations localmente (exemplo com Postgres via Docker)
1. Suba um Postgres local:
```bash
docker run --name pg-ci-cd -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ci_cd_fastapi -p 5433:5432 -d postgres:16
```

2. Aponte a DATABASE_URL e rode as migrations:
```bash 
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5433/ci_cd_fastapi"
alembic upgrade head
```

## 🔍 Como visualizar as tabelas e os dados do Postgres (Render)
Você pode inspecionar o banco usando um cliente PostgreSQL (recomendado: DBeaver).

1. No Render, abra o serviço do PostgreSQL do projeto

2. Clique em Connect (canto superior direito)

3. Use a aba External para pegar os dados/URL de conexão

4. No DBeaver:

- New Connection → PostgreSQL

- Cole host/porta/db/user/senha (ou a URL)

- Test Connection

- Vá em Schemas → public → Tables → (ex: pedidos) → View Data

Dica: em produção, a API cria/atualiza tabelas via migrations (Alembic). Se aparecer erro “table does not exist”, normalmente é migration que não rodou.

## ⚙️ CI/CD (GitHub Actions)
A cada push/PR na main, o workflow executa:

1. Instala dependências

2. Lint com ruff

3. Testes + cobertura com pytest --cov

4. Build da imagem Docker

5. Push no Docker Hub (tags latest + <sha-do-commit>)

## 💼 Por que isso importa em ambiente real?

- Qualidade: testes automáticos evitam regressões e falhas em produção

- Padronização: Docker garante ambiente reproduzível (sem “na minha máquina funciona”)

- Entrega contínua: cada mudança vira um artefato versionado (imagem Docker)

- Rastreabilidade: tags por commit permitem identificar exatamente o que foi publicado

- Manutenibilidade: migrations e Postgres deixam o projeto no padrão de empresa