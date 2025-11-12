from flask import render_template
from flask_login import login_required, current_user
from decorators import rol_required

@login_required
@rol_required(2)  # Solo donadores (rol 2)
def home():
    """Panel del donador"""
    return render_template('donador/home.html')

