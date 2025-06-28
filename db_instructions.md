# Como Acessar o Contêiner do Banco de Dados e Visualizar os Dados

Este guia fornece instruções sobre como se conectar ao contêiner do banco de dados PostgreSQL, listar suas tabelas e consultar os dados.

## 1. Conecte-se ao Contêiner do Banco de Dados

Para obter um shell `psql` interativo dentro do contêiner `db` em execução, execute o seguinte comando no seu terminal a partir da raiz do projeto:

```bash
docker exec -it db psql -U user -d mydatabase
```

-   `docker exec -it db`: Esta parte do comando instrui o Docker a executar um comando dentro do contêiner `db` em modo interativo (`-it`).
-   `psql -U user -d mydatabase`: Este é o comando que roda dentro do contêiner. Ele inicia o cliente `psql`, conectando-se como o usuário (`-U`) `user` ao banco de dados (`-d`) chamado `mydatabase`.

## 2. Listar Tabelas

Depois de se conectar e ver o prompt do `psql` (por exemplo, `mydatabase=#`), você pode listar todas as tabelas no banco de dados atual com o seguinte comando:

```sql
\dt
```

Isso exibirá uma lista de todas as tabelas criadas pelo usuário.

## 3. Consultar Dados (Exemplo)

Para ver todos os dados na sua tabela `todo`, você pode usar um comando `SELECT`.

```sql
SELECT * FROM todo;
```

Se você ainda não adicionou nenhuma tarefa pela interface web da aplicação, este comando não retornará nenhuma linha. Depois de adicionar tarefas, você verá os dados aqui.

**Exemplo de Saída:**

```
 id |    content     | completed
----+----------------+-----------
  1 | Minha primeira tarefa | f
  2 | Outra tarefa   | f
(2 rows)
```

## 4. Sair do PSQL

Para sair do shell `psql` e retornar ao prompt do seu terminal, digite `\q` e pressione Enter.

```sql
\q
```