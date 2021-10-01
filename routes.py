from recursos.autenticacao import Autenticacao
from recursos.usuario import UsuarioCadastro


def inicializa_rotas(api, bcrypt):
    api.add_resource(Autenticacao, "/autenticacao")
    api.add_resource(UsuarioCadastro, '/cadastro-usuario')