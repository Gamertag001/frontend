from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from src.database import get_db
from src.models.ModelUser import ModelUser

def index():
    """Redirige a la página de login"""
    return redirect(url_for('login'))

def login():
    """Maneja el login de usuarios"""
    if request.method == 'POST':
        username = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        db = get_db()
        if db:
            user = ModelUser.get_by_username(db, username)
            db.close()
            
            if user and user.password == password and user.correo == correo:
                login_user(user)
                flash(f'¡Bienvenido, {user.fullname}!', 'success')
                
                # Redirigir según el rol
                if user.id_rol == 1:  # Admin
                    return redirect(url_for('admin'))
                else:  # Donador
                    return redirect(url_for('home'))
            else:
                flash('Credenciales incorrectas. Por favor, intenta de nuevo.', 'error')
        else:
            flash('Error de conexión a la base de datos.', 'error')
    
    return render_template('auth/login.html')

def logout():
    """Cierra la sesión del usuario"""
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))

def register():
    """Maneja el registro de nuevos usuarios"""
    if request.method == 'POST':
        username = request.form.get('username')
        correo = request.form.get('correo')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        
        # Validar que todos los campos estén presentes
        if not all([username, correo, password, fullname]):
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('auth/register.html')
        
        db = get_db()
        if db:
            try:
                # Verificar si el usuario ya existe
                existing_user = ModelUser.get_by_username(db, username)
                if existing_user:
                    db.close()
                    flash('El nombre de usuario ya existe. Por favor, elige otro.', 'error')
                    return render_template('auth/register.html')
                
                # Crear nuevo usuario (rol 2 = donador por defecto)
                user_id = ModelUser.create(db, username, password, fullname, correo, id_rol=2)
                db.close()
                
                if user_id:
                    flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Error al crear la cuenta. Por favor, intenta de nuevo.', 'error')
            except Exception as e:
                db.close()
                print(f"Error en registro: {e}")
                flash('Error al procesar el registro. Por favor, verifica tus datos e intenta de nuevo.', 'error')
        else:
            flash('Error de conexión a la base de datos. Verifica que MySQL esté ejecutándose y que las credenciales sean correctas.', 'error')
    
    return render_template('auth/register.html')

