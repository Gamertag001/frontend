import mysql.connector
from config import config

def get_db():
    """Obtiene una conexión a la base de datos"""
    try:
        # Primero intentar conectar sin especificar la base de datos para crearla si no existe
        try:
            db = mysql.connector.connect(
                host=config['development'].MYSQL_HOST,
                user=config['development'].MYSQL_USER,
                password=config['development'].MYSQL_PASSWORD,
                database=config['development'].MYSQL_DB
            )
            return db
        except mysql.connector.Error as db_err:
            # Si la base de datos no existe, intentar crearla
            if db_err.errno == 1049:  # Error: Unknown database
                print(f"La base de datos no existe. Intentando crearla...")
                # Conectar sin especificar la base de datos
                temp_db = mysql.connector.connect(
                    host=config['development'].MYSQL_HOST,
                    user=config['development'].MYSQL_USER,
                    password=config['development'].MYSQL_PASSWORD
                )
                cursor = temp_db.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['development'].MYSQL_DB}")
                temp_db.commit()
                cursor.close()
                temp_db.close()
                
                # Ahora conectar a la base de datos recién creada
                db = mysql.connector.connect(
                    host=config['development'].MYSQL_HOST,
                    user=config['development'].MYSQL_USER,
                    password=config['development'].MYSQL_PASSWORD,
                    database=config['development'].MYSQL_DB
                )
                # Crear las tablas necesarias
                create_tables(db)
                return db
            else:
                raise db_err
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        print(f"Código de error: {err.errno}")
        print(f"Mensaje: {err.msg}")
        return None

def create_tables(db):
    """Crea las tablas necesarias si no existen"""
    try:
        cursor = db.cursor()
        
        # Crear tabla de roles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(50) NOT NULL
            )
        """)
        
        # Insertar roles por defecto
        cursor.execute("""
            INSERT IGNORE INTO roles (id, nombre) VALUES 
            (1, 'Administrador'),
            (2, 'Donador')
        """)
        
        # Crear tabla de usuarios
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
        
        # Crear tabla de donaciones (opcional)
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
        
        db.commit()
        cursor.close()
        print("Tablas creadas exitosamente")
    except mysql.connector.Error as err:
        print(f"Error al crear las tablas: {err}")
        db.rollback()

