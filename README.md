# Task Challenge - FastAPI

Este é um projeto de desafio que implementa uma simples aplicação de lista de tarefas (To-Do) usando FastAPI, SQLModel e PostgreSQL, totalmente containerizada com Docker.

## Sobre o Projeto

A aplicação fornece uma API para gerenciar tarefas e uma interface de usuário básica para interagir com elas. O projeto está estruturado para ser executado em ambientes de desenvolvimento e produção usando Docker Compose.

## Pré-requisitos

Para executar este projeto, você precisará ter o [Docker](https://www.docker.com/get-started) e o [Docker Compose](https://docs.docker.com/compose/install/) instalados em sua máquina.

## Configuração do Ambiente

Antes de iniciar a aplicação, você precisa configurar as variáveis de ambiente.

1.  **Crie um arquivo `.env`:**

    Na raiz do projeto, crie uma cópia do arquivo `.env.example` e renomeie-a para `.env`.

    ```bash
    cp .env.example .env
    ```

2.  **Revise as variáveis de ambiente (opcional):**

    Abra o arquivo `.env` e, se desejar, altere os valores. Para a execução padrão, os valores padrão devem funcionar sem problemas.

## Executando a Aplicação

O projeto é gerenciado com Docker Compose e possui configurações para dois ambientes distintos.

### Ambiente de Desenvolvimento

Para iniciar a aplicação em modo de desenvolvimento, execute o seguinte comando. Isso usará o `docker-compose.yml`.

```bash
docker compose up --build -d
```

-   O serviço da aplicação usará o `uvicorn` com `--reload`, então as alterações que você fizer no código-fonte na pasta `./app` serão refletidas automaticamente no contêiner.
-   O banco de dados armazenará seus dados em um volume local chamado `.postgres-data`.

### Ambiente de Produção

Para simular um ambiente de produção, use o arquivo `docker-compose.production.yml`.

```bash
docker compose -f docker-compose.production.yml up --build -d
```

-   Neste modo, o `uvicorn` é executado sem o recarregamento automático para melhor desempenho.

## Acessando a Aplicação

Depois de iniciar os contêineres, você pode acessar:

-   **Interface do Usuário:** [http://localhost:8000/](http://localhost:8000/)
-   **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Documentação Alternativa (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Acessando o Banco de Dados

Para instruções detalhadas sobre como se conectar diretamente ao contêiner do banco de dados para executar consultas SQL, consulte o arquivo [db_instructions.md](./db_instructions.md).
