from flask import Flask

#CREAR Y CONFIGURAR LA APICACION Flask
def crear_app():

    app = Flask(__name__)
    
    #CONFIGURACION BASICA DE LA APLICACION
    app.config['SECRET_KEY'] = 'proyecto_riego_automatizado_ipc2'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max para archivos
    
    #REGISTRAR BLUEPRINTS (rutas)
    from .controladores.main_controller import main_bp
    app.register_blueprint(main_bp)
    
    return app