from flask import Flask, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config
import mysql.connector

# Controladores
from src.controllers import auth_controller, admin_controller, donador_controller
from src.models.ModelUser import ModelUser
from src.database import get_db

app = Flask(__name__, static_folder='static image', template_folder='templates')
app.config.from_object(config['development'])

# Seguridad y login
csrf = CSRFProtect(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'




# Cargar usuario activo
@login_manager_app.user_loader
def load_user(id):
    db = get_db()
    user = ModelUser.get_by_id(db, id)
    db.close()
    return user


# ---------------------- RUTAS PRINCIPALES ----------------------

# rutas de AUTH
app.add_url_rule('/', view_func=auth_controller.index)
app.add_url_rule('/login', view_func=auth_controller.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=auth_controller.logout)
app.add_url_rule('/register', view_func=auth_controller.register, methods=['GET', 'POST'])

# rutas de ADMIN
app.add_url_rule('/admin', view_func=admin_controller.panel, endpoint='admin')

# rutas de DONADOR
app.add_url_rule('/home', view_func=donador_controller.home, endpoint='home')

# ---------------------- ERRORES ----------------------
def status_401(error):
    flash("Debes iniciar sesión para acceder a esta página.")
    return redirect(url_for('login'))

def status_404(error):
    return "Página no encontrada", 404


# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)
