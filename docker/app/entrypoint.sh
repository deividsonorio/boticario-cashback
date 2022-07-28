#!/bin/bash
# Espera até o banco postgres estar pronto para conecções
# Também permite executar comando após o banco estar disponível (migrate, runserver..)
function postgres_ready(){
python << END
import sys
import psycopg2
try:
    print("Trying to connect to database '$DB_NAME' on host '$DB_HOST'..")
    conn = psycopg2.connect(dbname="$DB_NAME", user="$DB_USER", password="$DB_PASSWORD", host="$DB_HOST")
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres não disponível - esperando..."
  sleep 1
done

>&2 echo "Postgres disponível - continuando..."
# Comando recebido é executado
exec "$@"