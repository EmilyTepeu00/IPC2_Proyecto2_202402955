from flask import Flask

#PARA CREAR LA APLICACION Flask
def crear_app():
    app = Flask(__name__)

    #Blueprint
    from .controladores.main_controller import main_bp
    app.register_blueprint(main_bp)

    return app