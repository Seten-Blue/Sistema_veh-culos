import time
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.database import SQLALCHEMY_DATABASE_URL, Base, engine

def wait_for_db():
    max_retries = 30
    retry_interval = 2

    for i in range(max_retries):
        try:
            # Intentar crear las tablas
            Base.metadata.create_all(bind=engine)
            print("Base de datos inicializada correctamente")
            return True
        except OperationalError as e:
            print(f"Intento {i + 1}/{max_retries}: No se puede conectar a la base de datos. Reintentando en {retry_interval} segundos...")
            time.sleep(retry_interval)
    
    print("No se pudo conectar a la base de datos después de varios intentos")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        sys.exit(1)