FROM python:3.13-slim

# Evitar arquivos .pyc e garantir logs no stdout
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:aplicacao", "--host", "0.0.0.0", "--port", "8000"]
