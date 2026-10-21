from fastapi import FastAPI, HTTPException
from schemas import ReservaCriacao
from services import criar_reserva
from repositories import listar_reservas, buscar_reserva_por_id
from excecoes import SalaIndisponivelError, PeriodoInvalidoError


app = FastAPI()


@app.get("/")
def inicio():
    return {
        "mensagem": "Roomly API funcionando"
    }


@app.get("/reservas")
def consultar_reservas() -> list[dict]:
    reservas = listar_reservas()

    return reservas


@app.get("/reservas/{reserva_id}")
def consultar_reserva(reserva_id: int) -> dict:
    reserva = buscar_reserva_por_id(reserva_id)

    if reserva is None:

        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada"
        )

    return reserva


@app.post("/reservas", status_code=201)
def cadastrar_reserva(dados: ReservaCriacao) -> dict:
    try:
        return criar_reserva(dados.model_dump())

    except SalaIndisponivelError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro)
        ) from erro

    except PeriodoInvalidoError as erro:
        raise HTTPException(
            status_code=422,
            detail=str(erro)
        ) from erro