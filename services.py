from datetime import datetime
from repositories import buscar_conflitos, inserir_reserva
from excecoes import SalaIndisponivelError, PeriodoInvalidoError


def validar_periodo(inicio: datetime, fim: datetime) -> None:
    if fim <= inicio:
        raise PeriodoInvalidoError("O fim deve ser posterior ao início")


def criar_reserva(nova_reserva: dict) -> dict:
    validar_periodo(nova_reserva["inicio"], nova_reserva["fim"])

    conflitos = buscar_conflitos(
        nova_reserva["id_sala"],
        nova_reserva["inicio"],
        nova_reserva["fim"]
    )

    if conflitos:
        raise SalaIndisponivelError("Sala indisponível neste horário")

    reserva = inserir_reserva(
        nova_reserva["id_usuario"],
        nova_reserva["id_sala"],
        nova_reserva["inicio"],
        nova_reserva["fim"]
    )

    return reserva