from flasgger import Swagger
from flask_restful import Api
from flask import Flask

from recursos.autenticacao import Autenticacao
from recursos.usuario import UsuarioRecurso


def inicializa_rotas(api: Api):
    api.add_resource(Autenticacao, "/autenticacao")
    api.add_resource(UsuarioRecurso, "/usuario")


def inicializa_swagger(app: Flask):
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

    swag = Swagger(app, config=swagger_config)

