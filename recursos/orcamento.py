import os
from urllib.parse import unquote

from flasgger import SwaggerView, swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from modelos.orcamento import (
    OrcamentoSchema,
    OrcamentoModel,
    OrcamentoGetParamSchema,
    OrcamentoResultadoQuerySchema,
    OrcamentoVisualizacaoSchema,
)

orcamento_schema = OrcamentoSchema()


class OrcamentoRecurso(SwaggerView):

    definitions = {
        "OrcamentoSchema": OrcamentoSchema,
        "OrcamentoGetParamSchema": OrcamentoGetParamSchema,
        "OrcamentoResultadoQuerySchema": OrcamentoResultadoQuerySchema,
        "OrcamentoVisualizacaoSchema": OrcamentoVisualizacaoSchema,
    }

    @jwt_required()
    @swag_from(f"swagger{os.sep}orcamento_put.yml", validation=False)
    def put(self):

        # Recupera os dados do usuário autenticado
        claims = get_jwt()
        id_usuario = claims["id"]

        # Recupera os dados enviados no corpo da requisição
        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = orcamento_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        # Adiciona o campo id_usuario
        dados["id_usuario"] = id_usuario

        # Instancia um novo Objeto do tipo Orcamento com os dados
        orcamento = OrcamentoModel(**dados)

        # Salva o objeto no bando de dados
        if orcamento.salva():
            res = OrcamentoVisualizacaoSchema()
            return res.dump(orcamento.retorna_dicionario()), 201
        else:
            return {"message": "Ocorreu um erro, tente novamente"}, 500


class OrcamentoIDRecurso(SwaggerView):

    definitions = {
        "OrcamentoSchema": OrcamentoSchema,
        "OrcamentoGetParamSchema": OrcamentoGetParamSchema,
        "OrcamentoResultadoQuerySchema": OrcamentoResultadoQuerySchema,
        "OrcamentoVisualizacaoSchema": OrcamentoVisualizacaoSchema,
    }

    @jwt_required()
    @swag_from(f"swagger{os.sep}orcamento_get.yml", validation=False)
    def get(self, _id):

        # Recupera os dados do usuário autenticado
        claims = get_jwt()
        _id_usuario = claims["id"]

        _orcamento = OrcamentoModel.busca_por_id_e_usuario(
            _id=_id, _id_usuario=_id_usuario
        )

        return _orcamento, 200 if _orcamento else 404

    @jwt_required()
    @swag_from(f"swagger{os.sep}orcamento_post.yml", validation=False)
    def post(self, _id):

        claims = get_jwt()
        id_usuario = claims["id"]

        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = orcamento_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        orcamento = OrcamentoModel.busca_por_id(_id=_id)

        if orcamento:
            for chave, valor in dados.items():
                setattr(orcamento, chave, valor)

            if orcamento.salva():
                res = OrcamentoVisualizacaoSchema()
                return res.dump(orcamento.retorna_dicionario()), 200
            else:
                return {"message": "Ocorreu um erro, tente novamente"}, 500
        else:
            return {"message": "Orçamento não localizado"}, 404

    @jwt_required()
    @swag_from(f"swagger{os.sep}orcamento_delete.yml", validation=False)
    def delete(self, _id):

        claims = get_jwt()
        id_usuario = claims["id"]

        registro = OrcamentoModel.remove_por_id_e_id_usuario(_id_usuario=id_usuario, _id=_id)

        if registro is True:
            return
        elif registro is None:
            return {"message": "Registro não localizado"}, 404
        else:
            return {"message": "Ocorreu um erro ao tentar excluir o registro"}, 500


class OrcamentosRecurso(SwaggerView):

    definitions = {
        "OrcamentoSchema": OrcamentoSchema,
        "OrcamentoGetParamSchema": OrcamentoGetParamSchema,
        "OrcamentoResultadoQuerySchema": OrcamentoResultadoQuerySchema,
    }

    @jwt_required()
    @swag_from(f"swagger{os.sep}orcamentos_get.yml", validation=False)
    def get(self):

        url_parametros = OrcamentoGetParamSchema()

        try:
            dados = url_parametros.load(request.args)
        except ValidationError as err:
            return err.messages, 422

        # Recupera os dados do usuário autenticado
        claims = get_jwt()
        _id_usuario = claims["id"]

        _orcamentos = []

        if dados["id"] > 0:
            _orcamentos = OrcamentoModel.busca_por_id_e_usuario(
                _id=dados["id"], _id_usuario=_id_usuario
            )
        else:
            _orcamentos = OrcamentoModel.busca_por_nome_ou_identidade(
                _id_usuario=_id_usuario,
                _nome=unquote(dados["nome"]) if dados["nome"] else None,
                _identidade=unquote(dados["identidade"])
                if dados["identidade"]
                else None,
                _pagina=dados["pagina"],
                _limite=dados["limite"],
            )

        return _orcamentos, 200
