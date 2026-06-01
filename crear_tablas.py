from database import obtener_conexion

def inicializar_base_de_datos():
    print("⏳ Conectando a la nube de Aiven para configurar tablas...")
    conexion = obtener_conexion()
    if not conexion:
        print("❌ No se pudo establecer la conexión.")
        return

    cursor = conexion.cursor()
    
    # 1. Eliminamos tablas viejas para evitar conflictos de columnas
    print("🧹 Limpiando residuos anteriores...")
    cursor.execute("DROP TABLE IF EXISTS usuarios;")
    
    # 2. Creamos la tabla definitiva con soporte para correo y avatar
    print("🏗️ Creando la tabla de usuarios definitiva...")
    tabla_usuarios = """
    CREATE TABLE usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        avatar VARCHAR(50) DEFAULT 'avatar1.png',
        puntuacion_total INT DEFAULT 0,
        nivel_progreso INT DEFAULT 1
    );
    """
    cursor.execute(tabla_usuarios)
    conexion.commit()
    
    print("🚀 ¡TABLAS CONFIGURADAS CON ÉXITO EN LA NUBE!")
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    inicializar_base_de_datos()