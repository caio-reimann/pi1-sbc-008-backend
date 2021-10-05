from recursos.autenticacao import Autenticacao
from recursos.usuario import UsuarioRecurso


def inicializa_rotas(api, bcrypt):
    api.add_resource(Autenticacao, "/autenticacao")
    api.add_resource(UsuarioRecurso, '/usuario')