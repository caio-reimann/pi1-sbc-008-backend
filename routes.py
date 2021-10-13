from flask_apispec import FlaskApiSpec
from flask_restful import Api

from recursos.autenticacao import Autenticacao
from recursos.usuario import UsuarioRecurso


def inicializa_rotas(api: Api):
    api.add_resource(Autenticacao, "/autenticacao")
    api.add_resource(UsuarioRecurso, "/usuario")


def inicializa_documentacao(docs: FlaskApiSpec):
    docs.register(Autenticacao)
    docs.register(UsuarioRecurso)
