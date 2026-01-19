from fastapi import FastAPI

aplicacao = FastAPI(title="API Demonstração CI/CD")


@aplicacao.get("/saude")
def verificar_saude():
    return {"status": "ok"}


@aplicacao.get("/itens/{id_item}")
def buscar_item(id_item: int):
    return {"id_item": id_item, "descricao": f"Item número {id_item}"}
