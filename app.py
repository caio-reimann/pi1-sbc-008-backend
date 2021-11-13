import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api

from config import inicializa_swagger
from db import db_session, init_db

from routes import inicializa_rotas

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# Inicialização de outras bibliotecas
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
swagger = inicializa_swagger(app=app)

inicializa_rotas(api=api)


@app.teardown_request
def checkin_db(exc):
    try:
        db_session.remove()
    except:
        pass


@app.before_first_request
def first_request():
    init_db(bcrypt=bcrypt)


@app.errorhandler(404)
def page_not_found(e):
    return {"message": "Url não encontrada"}, 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return {"message": "Ocorreu um erro no Servidor, tente novamente"}, 500


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return {"message": "Token inválido ou expirado"}, 401


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
