from flask_login import UserMixin
from src.database import get_db

class ModelUser(UserMixin):
    def __init__(self, id, username, password, fullname, correo, id_rol):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.correo = correo
        self.id_rol = id_rol

    @staticmethod
    def get_by_id(db, id):
        """Obtiene un usuario por su ID"""
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data:
                return ModelUser(
                    id=user_data['id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    fullname=user_data['fullname'],
                    correo=user_data['correo'],
                    id_rol=user_data['id_rol']
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    @staticmethod
    def get_by_username(db, username):
        """Obtiene un usuario por su nombre de usuario"""
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data:
                return ModelUser(
                    id=user_data['id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    fullname=user_data['fullname'],
                    correo=user_data['correo'],
                    id_rol=user_data['id_rol']
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None

    @staticmethod
    def create(db, username, password, fullname, correo, id_rol=2):
        """Crea un nuevo usuario"""
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, password, fullname, correo, id_rol) VALUES (%s, %s, %s, %s, %s)",
                (username, password, fullname, correo, id_rol)
            )
            db.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return user_id
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            db.rollback()
            return None

