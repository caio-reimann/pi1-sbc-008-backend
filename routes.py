
from flask_restful import Api


from recursos.autenticacao import Autenticacao
from recursos.usuario import UsuarioRecurso, UsuarioSenhaRecurso, UsuarioRecuperaSenhaRecurso


def inicializa_rotas(api: Api):
    api.add_resource(Autenticacao, "/autenticacao")
    api.add_resource(UsuarioRecurso, "/usuario")
    api.add_resource(UsuarioSenhaRecurso, "/alterasenha")
    api.add_resource(UsuarioRecuperaSenhaRecurso, "/recupera-senha")

