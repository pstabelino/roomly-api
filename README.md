
# Roomly API

API REST para gerenciamento de reservas de salas, desenvolvida em Python como parte de uma trilha prática de estudos em desenvolvimento backend.

O projeto permite cadastrar e consultar reservas, validar horários e impedir conflitos de agendamento, utilizando regras de negócio na aplicação e restrições de integridade no PostgreSQL.

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- PostgreSQL
- Psycopg 3
- Uvicorn

## Funcionalidades

- Criar reservas de salas
- Listar todas as reservas
- Consultar reservas por ID
- Validar períodos de reserva
- Impedir reservas sobrepostas na mesma sala
- Tratar exceções de negócio
- Retornar códigos HTTP adequados para cada situação

## Estrutura do projeto

```text
roomly/
├── banco.py
├── excecoes.py
├── main.py
├── repositories.py
├── schemas.py
├── services.py
├── requirements.txt
├── README.md
├── .gitignore
└── sql/
    ├── schema.sql
    └── consultas_exemplo.sql
```

### Responsabilidade dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Define os endpoints da API e as respostas HTTP |
| `schemas.py` | Define os modelos de entrada com Pydantic |
| `services.py` | Implementa as regras de negócio |
| `repositories.py` | Executa as operações SQL no PostgreSQL |
| `banco.py` | Centraliza a conexão com o banco |
| `excecoes.py` | Define exceções personalizadas |
| `sql/schema.sql` | Cria as tabelas e restrições do banco |
| `sql/consultas_exemplo.sql` | Contém consultas utilizadas nos estudos |

## Banco de dados

O Roomly utiliza PostgreSQL com três tabelas principais:

- **usuarios:** armazena os usuários.
- **salas:** armazena as salas e suas capacidades.
- **reservas:** registra os agendamentos, relacionando usuários e salas.

### Criando o banco

Com o PostgreSQL instalado e em execução, crie o banco de dados:

```sql
CREATE DATABASE roomly;
```

Em seguida, execute o arquivo `sql/schema.sql` no banco `roomly` para criar as tabelas e as restrições necessárias.

Pelo terminal, uma opção é:

```bash
psql -d roomly -f sql/schema.sql
```

Esse comando pressupõe que o usuário PostgreSQL configurado possui as permissões necessárias.

### Proteção contra reservas sobrepostas

Além da validação feita pelo Python, o banco utiliza uma `EXCLUDE CONSTRAINT` para impedir reservas conflitantes na mesma sala.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE reservas
ADD CONSTRAINT reservas_sem_sobreposicao
EXCLUDE USING gist (
    id_sala WITH =,
    tsrange(inicio, fim, '[)') WITH &&
);
```

Essa restrição também protege os dados quando duas requisições tentam reservar a mesma sala simultaneamente.

Reservas consecutivas, como 10h–11h e 11h–12h, são permitidas.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/pstabelino/roomly-api.git
cd roomly-api
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o PostgreSQL

Certifique-se de que o PostgreSQL esteja em execução e de que o banco `roomly` tenha sido criado com a estrutura definida em `sql/schema.sql`.

A conexão está centralizada em `banco.py` e utiliza as configurações locais do PostgreSQL.

Para ambientes diferentes, pode ser necessário ajustar os parâmetros de conexão. Em uma evolução futura, essas configurações poderão ser externalizadas em variáveis de ambiente.

### 5. Iniciar a API

```bash
uvicorn main:app --reload
```

A API estará disponível em:

http://127.0.0.1:8000

A documentação interativa do FastAPI estará disponível em:

http://127.0.0.1:8000/docs

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando |
| POST | `/reservas` | Cria uma reserva |
| GET | `/reservas` | Lista todas as reservas |
| GET | `/reservas/{reserva_id}` | Consulta uma reserva por ID |

### Exemplo de criação de reserva

**POST `/reservas`**

```json
{
  "id_usuario": 1,
  "id_sala": 1,
  "inicio": "2026-11-10T09:00:00",
  "fim": "2026-11-10T10:00:00"
}
```

Os IDs informados precisam corresponder a um usuário e a uma sala previamente cadastrados no banco.

### Respostas HTTP

| Código | Significado |
|---|---|
| `201 Created` | Reserva criada com sucesso |
| `200 OK` | Consulta realizada com sucesso |
| `404 Not Found` | Reserva não encontrada |
| `409 Conflict` | Sala indisponível no período solicitado |
| `422 Unprocessable Entity` | Dados ou período de reserva inválidos |

## Regras de negócio

1. O horário final deve ser posterior ao horário inicial.
2. Uma sala não pode possuir reservas com horários sobrepostos.
3. Reservas consecutivas são permitidas.
4. A disponibilidade é verificada na aplicação e protegida no banco de dados.
5. Cada reserva deve estar vinculada a um usuário e a uma sala existentes.

## Arquitetura

O projeto utiliza separação de responsabilidades:

```text
Cliente HTTP
    |
    v
FastAPI (main.py)
    |
    v
Service (services.py)
    |
    v
Repository (repositories.py)
    |
    v
PostgreSQL
```

A camada de API recebe requisições e retorna respostas HTTP.

A camada de serviço implementa as regras de negócio.

A camada de repositório realiza as operações de persistência no banco de dados.

## Aprendizados do projeto

- Desenvolvimento de APIs REST com FastAPI
- Validação de dados com Pydantic
- Organização de código em camadas
- Integração com PostgreSQL usando Psycopg
- Consultas SQL parametrizadas
- Integridade referencial
- Tratamento de exceções personalizadas
- Proteção contra conflitos de concorrência
- Versionamento com Git e GitHub

## Limitações e melhorias futuras

O Roomly é um projeto educacional e ainda não está preparado para uso em produção.

Entre as possíveis evoluções estão:

- Autenticação e autorização
- Configuração de conexão por variáveis de ambiente
- Tratamento de fusos horários
- Testes automatizados
- Paginação e filtros
- Containerização com Docker
- Deploy em servidor

## Autor

**Paulo Henrique**

Projeto desenvolvido como parte de uma jornada prática de aprendizado em Python e engenharia backend.
