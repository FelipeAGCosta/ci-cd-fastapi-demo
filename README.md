![CI](https://github.com/FelipeAGCosta/ci-cd-fastapi-demo/actions/workflows/ci.yml/badge.svg)

# API CI/CD com FastAPI, Docker e GitHub Actions

API em **Python (FastAPI)** com **testes automatizados (pytest)**, empacotada em **Docker** e validada automaticamente via **GitHub Actions** a cada push/PR na branch `main`.

## ✅ O que este projeto demonstra
- Criação de API REST com FastAPI
- Testes automatizados com `pytest`
- Containerização com Docker
- Pipeline de CI no GitHub Actions (testes + build de imagem)

## 🚀 Endpoints principais
- `GET /saude` → verifica se a API está respondendo
- `GET /docs` → documentação Swagger
- `POST /pedidos` → cria pedido
- `GET /pedidos` → lista pedidos
- `GET /pedidos/{id_pedido}` → busca pedido
- `PATCH /pedidos/{id_pedido}/status` → atualiza status do pedido

## ▶️ Rodar local (sem Docker)
```bash
pip install -r requirements.txt
pytest
uvicorn app.main:aplicacao --reload

Acesse:

http://127.0.0.1:8000/saude

http://127.0.0.1:8000/docs

🐳 Rodar com Docker
docker build -t ci-cd-fastapi-demo:dev .
docker run --rm -p 8000:8000 ci-cd-fastapi-demo:dev

⚙️ CI/CD (GitHub Actions)

A cada push/PR na main, o workflow:

instala dependências

roda testes (pytest)

faz build da imagem Docker

💼 Este repositório foi criado para demonstrar, na prática, um fluxo profissional de entrega:
código versionado → testes automatizados → build de artefato (Docker) → validação automática no CI.

