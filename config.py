import os
from flask import Flask
from flasgger import Swagger

class Config:
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_POOL_SIZE = 3
    DB_MAX_OVERFLOW = 2

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "univesptec@gmail.com"
    MAIL_PASSWORD = "1cde5d9cc2a1a80c4bb2468e92b"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def inicializa_swagger(app: Flask) -> Swagger:
    """
    Configurações do Flasgger (Swagger) para  geração da documentação
    :param app: App instaciado (Flask)
    :return:
    """
    swagger_config = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "securityDefinitions": {
            "bearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
            }
        }
    }

    return Swagger(app, config=swagger_config)
