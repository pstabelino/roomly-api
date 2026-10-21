import psycopg
from psycopg.rows import dict_row


def conectar():
    return psycopg.connect(
        dbname="roomly",
        row_factory=dict_row
    )