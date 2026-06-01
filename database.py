import os
from dotenv import load_dotenv
import mysql.connector

# Carga las variables del archivo .env
load_dotenv()

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"❌ Error al conectar a MySQL en la nube: {error}")
        return None

# Prueba rápida de conexión
if __name__ == "__main__":
    print("⏳ Intentando conectar a Aiven...")
    db = obtener_conexion()
    if db and db.is_connected():
        print("🚀 ¡CONEXIÓN EXITOSA! Tu Python ya habla con la nube.")
        db.close()