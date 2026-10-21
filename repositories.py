from datetime import datetime
from banco import conectar
from psycopg.errors import ExclusionViolation
from excecoes import SalaIndisponivelError


def buscar_conflitos(
    id_sala: int,
    inicio: datetime,
    fim: datetime
) -> list[dict]:

    with conectar() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM reservas
                WHERE id_sala = %s
                AND fim > %s
                AND inicio < %s;
                """,
                (id_sala, inicio, fim)
            )

            reservas = cursor.fetchall()

    return reservas


def inserir_reserva(
    id_usuario: int,
    id_sala: int,
    inicio: datetime,
    fim: datetime
) -> dict:

    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO reservas (
                        id_usuario,
                        id_sala,
                        inicio,
                        fim
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING
                        id,
                        id_usuario,
                        id_sala,
                        inicio,
                        fim,
                        criado_em;
                    """,
                    (id_usuario, id_sala, inicio, fim)
                )

                reserva = cursor.fetchone()

    except ExclusionViolation as erro:
        raise SalaIndisponivelError("Sala indisponível neste horário") from erro

    return reserva


def listar_reservas() -> list[dict]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM reservas
                ORDER BY inicio;
                """
            )

            reservas = cursor.fetchall()

    return reservas


def buscar_reserva_por_id(reserva_id: int) -> dict | None:
    with conectar() as conexao:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM reservas
                WHERE id = %s;
                """,
                (reserva_id,)
            )

            reserva = cursor.fetchone()

    return reserva