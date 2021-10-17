from flask_restful import Api


from recursos.autenticacao import Autenticacao
from recursos.geral import Inicio
from recursos.orcamento import OrcamentoRecurso, OrcamentosRecurso
from recursos.usuario import (
    UsuarioRecurso,
    UsuarioSenhaRecurso,
    UsuarioRecuperaSenhaRecurso,
)


def inicializa_rotas(api: Api):
    api.add_resource(Inicio, "/")

    api.add_resource(Autenticacao, "/autenticacao")
    api.add_resource(UsuarioRecurso, "/usuario")
    api.add_resource(UsuarioSenhaRecurso, "/alterasenha")
    api.add_resource(UsuarioRecuperaSenhaRecurso, "/recupera-senha")
    api.add_resource(OrcamentoRecurso, "/orcamento/<int:_id>")
    api.add_resource(OrcamentosRecurso, "/orcamentos")
