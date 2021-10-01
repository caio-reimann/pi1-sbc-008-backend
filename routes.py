from recursos.autenticacao import Autenticacao


def inicializa_rotas(api, bcrypt):
    api.add_resource(Autenticacao, "/auth")
