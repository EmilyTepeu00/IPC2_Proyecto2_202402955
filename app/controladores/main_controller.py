from flask import Blueprint

#Crear blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def pagina_inicio():
    return "Sistema de Riego Automatizado"