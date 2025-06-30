import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

print("Waiting for database connection...")

# Pega a URL do banco de dados da variável de ambiente
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# Tenta conectar ao banco de dados em um loop
max_retries = 30
retries = 0
while retries < max_retries:
    try:
        # Tenta criar uma conexão
        engine = create_engine(db_url)
        with engine.connect() as connection:
            print("Database connection successful!")
            break  # Sai do loop se a conexão for bem-sucedida
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        retries += 1
        print(f"Retrying in 2 seconds... ({retries}/{max_retries})")
        time.sleep(2)
else:
    print("Could not connect to the database after several retries. Exiting.")
    exit(1) # Termina com erro se não conseguir conectaior