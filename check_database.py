"""
Script para verificar y crear la base de datos
Ejecuta este script para verificar la conexión y crear las tablas necesarias
"""

import mysql.connector
from config import config

def check_and_create_database():
    """Verifica y crea la base de datos si no existe"""
    try:
        # Conectar sin especificar la base de datos
        print("Conectando a MySQL...")
        temp_db = mysql.connector.connect(
            host=config['development'].MYSQL_HOST,
            user=config['development'].MYSQL_USER,
            password=config['development'].MYSQL_PASSWORD
        )
        print("✓ Conexión a MySQL exitosa")
        
        cursor = temp_db.cursor()
        
        # Crear base de datos si no existe
        print(f"Verificando base de datos '{config['development'].MYSQL_DB}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['development'].MYSQL_DB}")
        print(f"✓ Base de datos '{config['development'].MYSQL_DB}' lista")
        
        cursor.close()
        temp_db.close()
        
        # Conectar a la base de datos
        db = mysql.connector.connect(
            host=config['development'].MYSQL_HOST,
            user=config['development'].MYSQL_USER,
            password=config['development'].MYSQL_PASSWORD,
            database=config['development'].MYSQL_DB
        )
        
        cursor = db.cursor()
        
        # Crear tabla de roles
        print("Creando tabla de roles...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(50) NOT NULL
            )
        """)
        print("✓ Tabla 'roles' creada")
        
        # Insertar roles por defecto
        cursor.execute("""
            INSERT IGNORE INTO roles (id, nombre) VALUES 
            (1, 'Administrador'),
            (2, 'Donador')
        """)
        print("✓ Roles insertados")
        
        # Crear tabla de usuarios
        print("Creando tabla de usuarios...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fullname VARCHAR(100) NOT NULL,
                correo VARCHAR(100) NOT NULL,
                id_rol INT NOT NULL DEFAULT 2,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_rol) REFERENCES roles(id)
            )
        """)
        print("✓ Tabla 'usuarios' creada")
        
        # Crear tabla de donaciones
        print("Creando tabla de donaciones...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donaciones (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT NOT NULL,
                monto DECIMAL(10, 2) NOT NULL,
                categoria VARCHAR(50),
                mensaje TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
            )
        """)
        print("✓ Tabla 'donaciones' creada")
        
        db.commit()
        cursor.close()
        db.close()
        
        print("\n✅ Base de datos configurada correctamente!")
        print("Ahora puedes ejecutar la aplicación Flask.")
        
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")
        print(f"Código de error: {err.errno}")
        print("\nPosibles soluciones:")
        print("1. Verifica que MySQL esté ejecutándose")
        print("2. Verifica las credenciales en config.py")
        print("3. Asegúrate de que el usuario tenga permisos para crear bases de datos")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == '__main__':
    check_and_create_database()

