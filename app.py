import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, Blueprint
from flask_apispec import FlaskApiSpec
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from db import db_session, init_db

from routes import inicializa_rotas, inicializa_documentacao

app = Flask(__name__)
api = Api(app)

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Projeto PI1 - Software Gerador de Propostas para Prestação de Pequenos Serviços',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

inicializa_rotas(api=api)
inicializa_documentacao(docs=docs)


@app.teardown_request
def checkin_db(exc):
    try:
        db_session.remove()
    except:
        pass


@app.before_first_request
def first_request():
    init_db(bcrypt=bcrypt)


if __name__ == "__main__":
    app.run()
