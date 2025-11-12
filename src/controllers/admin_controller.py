from flask import render_template
from flask_login import login_required, current_user
from decorators import rol_required

@login_required
@rol_required(1)  # Solo administradores (rol 1)
def panel():
    """Panel de administración"""
    return render_template('admin/panel.html')

