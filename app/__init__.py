from flask import Flask
from .routes import main, registro, pedidos, login
from . import db

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",  # <- le dice dónde buscar los HTML
        static_folder="../static"       # <- si tienes archivos estáticos
    )

    
    # Registrar blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(registro.bp)
    app.register_blueprint(pedidos.bp)
    app.register_blueprint(login.bp)


    return app
