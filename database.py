import os
from dotenv import load_dotenv
import mysql.connector

# Carga las variables del archivo .env
load_dotenv()

def obtener_conexion():
    try:
        host = os.getenv("DB_HOST")
        port_env = os.getenv("DB_PORT")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")

        # Safe port parsing: default to 3306 if not set or invalid
        try:
            port = int(port_env) if port_env else 3306
        except (ValueError, TypeError):
            port = 3306

        conexion = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return conexion
    except Exception as error:
        # Capturamos cualquier excepción (no solo mysql.connector.Error)
        print(f"❌ Error al conectar a MySQL en la nube: {error}")
        return None

# Prueba rápida de conexión
if __name__ == "__main__":
    print("⏳ Intentando conectar a Aiven...")
    db = obtener_conexion()
    if db and db.is_connected():
        print("🚀 ¡CONEXIÓN EXITOSA! Tu Python ya habla con la nube.")
        db.close()