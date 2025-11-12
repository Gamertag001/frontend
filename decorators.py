from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def rol_required(*roles):
    """
    Decorador para restringir rutas a ciertos roles.
    Ejemplo:
        @rol_required(1)
        @rol_required(1, 2)
        @rol_required('admin')
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar si el usuario está logueado
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a esta página.")
                return redirect(url_for('login'))

            # Verificar si el rol del usuario coincide con los roles permitidos
            if current_user.id_rol not in roles:
                flash("No tienes permiso para acceder a esta página.")
                return redirect(url_for('login'))

            #Si todo bien, continuar
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
