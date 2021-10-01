from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from modelos.usuario import CadastramentoUsuarioSchema, UsuarioModel


usuario_cadastro_schema = CadastramentoUsuarioSchema()


class UsuarioCadastro(Resource):
    """ """
    def put(self):
        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = usuario_cadastro_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        duplicidade = UsuarioModel.busca_por_duplicidade(_email=dados["email"], _identidade=dados["identidade"])

        if duplicidade:
            if duplicidade.identidade == dados["identidade"]:
                if len(dados["identidade"]) == 18:
                    return {"message": "CNPJ já cadastrado."}, 400
                else:
                    return {"message": "CPF já cadastrado."}, 400
            elif duplicidade.email == dados["email"]:
                return {"message": "Email já cadastrado."}, 400

        usuario = UsuarioModel(**dados)

        if usuario.salva():
            return {"message": "Usuário cadastrado com sucesso."}, 201
        else:
            return {"message": "Ocorreu um erro, tente novamente"}, 500

