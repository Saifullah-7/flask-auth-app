from flask import Flask
from .models.user_model import db
import config
from .routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(auth_bp)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
