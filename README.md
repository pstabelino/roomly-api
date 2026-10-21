
# Roomly API

API REST para gerenciamento de reservas de salas, desenvolvida como projeto de estudos em Python e desenvolvimento backend.

## Tecnologias

- Python
- FastAPI
- Pydantic
- PostgreSQL
- Psycopg 3

## Funcionalidades

- Criar reservas de salas
- Listar reservas
- Consultar uma reserva por ID
- Validar períodos de reserva
- Impedir reservas sobrepostas para a mesma sala
- Tratar erros de negócio com códigos HTTP adequados

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando |
| POST | `/reservas` | Cria uma reserva |
| GET | `/reservas` | Lista todas as reservas |
| GET | `/reservas/{reserva_id}` | Consulta uma reserva |

## Regras de negócio

O horário final deve ser posterior ao horário inicial.

Reservas da mesma sala não podem ter períodos sobrepostos. Essa regra é verificada na aplicação e protegida no PostgreSQL por uma exclusion constraint.

## Executando localmente

1. Crie um ambiente virtual Python.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Configure o PostgreSQL e crie as tabelas necessárias.
4. Inicie a API:

```bash
uvicorn main:app --reload
```

A documentação interativa estará disponível em:

`http://127.0.0.1:8000/docs`

## Status

Projeto educacional concluído como parte de uma trilha de desenvolvimento backend.
