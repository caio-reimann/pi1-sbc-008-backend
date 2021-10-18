from flask_restful import Api


from recursos.autenticacao import Autenticacao
from recursos.geral import Inicio
from recursos.item_orcamento import ItemOrcamentoRecurso, ItensOrcamentoRecurso, ItemOrcamentoIDRecurso
from recursos.orcamento import OrcamentoRecurso, OrcamentosRecurso, OrcamentoIDRecurso
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
    api.add_resource(OrcamentoIDRecurso, "/orcamento/<int:_id>")
    api.add_resource(OrcamentoRecurso, "/orcamento")
    api.add_resource(OrcamentosRecurso, "/orcamentos")
    api.add_resource(ItemOrcamentoIDRecurso, "/item_orcamento/<int:_id>")
    api.add_resource(ItemOrcamentoRecurso, "/item_orcamento")
    api.add_resource(ItensOrcamentoRecurso, "/itens_orcamento/<int:_id_orcamento>")
