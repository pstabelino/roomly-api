from datetime import datetime
from pydantic import BaseModel


class ReservaCriacao(BaseModel):
    id_usuario: int
    id_sala: int
    inicio: datetime
    fim: datetime