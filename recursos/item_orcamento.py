import os

from flasgger import SwaggerView, swag_from
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from modelos.item_orcamento import ItemOrcamentoModel, ItemOrcamentoSchema, ItemOrcamentoGetParamSchema, \
    ItemOrcamentoResultadoQuerySchema, ItemOrcamentoIDSchema
from modelos.orcamento import OrcamentoModel

item_orcamento_schema = ItemOrcamentoSchema()


class ItemOrcamentoRecurso(SwaggerView):

    definitions = {
        "ItemOrcamentoSchema": ItemOrcamentoSchema,
        "ItemOrcamentoIDSchema": ItemOrcamentoIDSchema
    }

    @jwt_required()
    @swag_from(f"swagger{os.sep}item_orcamento_put.yml", validation=False)
    def put(self):

        # Recupera os dados do usuário autenticado
        claims = get_jwt()
        id_usuario = claims["id"]

        # Recupera os dados enviados no corpo da requisição
        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = item_orcamento_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        # Adiciona o campo id_usuario
        dados["id_usuario"] = id_usuario

        orcamento = OrcamentoModel.busca_por_id_e_id_usuario(_id=dados["id_orcamento"], _id_usuario=dados["id_usuario"])

        if orcamento:

            # Instancia um novo Objeto do tipo Orcamento com os dados
            item_orcamento = ItemOrcamentoModel(**dados)

            # Salva o objeto no bando de dados
            if item_orcamento.salva():
                dados["id"] = item_orcamento.id
                return dados, 201
            else:
                return {"message": "Ocorreu um erro, tente novamente"}, 500
        else:
            return {"message": "Orçamento não encontrado"}, 404


class ItemOrcamentoIDRecurso(SwaggerView):

    definitions = {
        "ItemOrcamentoSchema": ItemOrcamentoSchema,
    }

    @jwt_required()
    @swag_from(f"swagger{os.sep}item_orcamento_get.yml", validation=False)
    def get(self, _id):

        # Recupera os dados do usuário autenticado
        claims = get_jwt()
        _id_usuario = claims["id"]

        _item_orcamento = ItemOrcamentoModel.busca_por_id_e_id_usuario(
            _id=_id, _id_usuario=_id_usuario
        )

        return _item_orcamento, 200 if _item_orcamento else 404

    @jwt_required()
    @swag_from(f"swagger{os.sep}item_orcamento_post.yml", validation=False)
    def post(self, _id):

        claims = get_jwt()
        id_usuario = claims["id"]

        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = item_orcamento_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        item_orcamento = ItemOrcamentoModel.busca_por_id_e_id_usuario(_id_usuario=id_usuario, _id=_id, _id_orcamento=dados["id_orcamento"])

        if item_orcamento:
            for chave, valor in dados.items():
                setattr(item_orcamento, chave, valor)

            if item_orcamento.salva():
                res = ItemOrcamentoIDSchema()
                return res.dump(item_orcamento.retorna_dicionario()), 200
            else:
                return {"message": "Ocorreu um erro, tente novamente"}, 500
        else:
            return {"message": "Item não localizado"}, 404

    @jwt_required()
    @swag_from(f"swagger{os.sep}item_orcamento_delete.yml", validation=False)
    def delete(self, _id):

        claims = get_jwt()
        id_usuario = claims["id"]

        item_orcamento = ItemOrcamentoModel.remove_por_id_e_id_usuario(_id_usuario=id_usuario, _id=_id)

        if item_orcamento is True:
            return
        elif item_orcamento is None:
            return {"message": "Registro não localizado"}, 404
        else:
            return {"message": "Ocorreu um erro ao tentar excluir o registro"}, 500


class ItensOrcamentoRecurso(SwaggerView):

    definitions = {
        "ItemOrcamentoSchema": ItemOrcamentoSchema,
        "ItemOrcamentoGetParamSchema": ItemOrcamentoGetParamSchema,
        "ItemOrcamentoResultadoQuerySchema": ItemOrcamentoResultadoQuerySchema,
    }

    @jwt_required()
    @swag_from(f"swagger{os.sep}itens_orcamento_get.yml", validation=False)
    def get(self, _id_orcamento):

        url_parametros = ItemOrcamentoGetParamSchema()

        try:
            dados = url_parametros.load(request.args)
        except ValidationError as err:
            return err.messages, 422

        # Recupera os dados do usuário autenticado
        claims = get_jwt()
        _id_usuario = claims["id"]

        _itens = []

        _itens = ItemOrcamentoModel.busca_por_id_orcamento_e_id_usuario(
            _id_orcamento=_id_orcamento,
            _id_usuario=_id_usuario,
        )

        return _itens, 200
