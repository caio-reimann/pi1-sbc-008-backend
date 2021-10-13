import os

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource
from marshmallow import ValidationError


from modelos.usuario import (
    CadastramentoUsuarioSchema,
    UsuarioModel,
    AlteracaoUsuarioSchema,
)

usuario_cadastro_schema = CadastramentoUsuarioSchema()
usuario_alteracao_schema = AlteracaoUsuarioSchema(
    exclude=(
        "password",
        "aceite_termo",
    )
)


class UsuarioRecurso(Resource):
    """ """

    def put(self):
        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = usuario_cadastro_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        duplicidade = UsuarioModel.busca_por_duplicidade(
            _email=dados["email"], _identidade=dados["identidade"]
        )

        if duplicidade:
            if duplicidade.identidade == dados["identidade"]:
                if len(dados["identidade"]) == 18:
                    return {"message": "CNPJ já cadastrado."}, 400
                else:
                    return {"message": "CPF já cadastrado."}, 400
            elif duplicidade.email == dados["email"]:
                return {"message": "Email já cadastrado."}, 400

        from app import bcrypt

        dados["password"] = bcrypt.generate_password_hash(
            os.environ.get("DB_ADMIN_PASSWORD")
        ).decode("utf-8")

        dados.pop("cpassword")

        usuario = UsuarioModel(**dados)

        if usuario.salva():
            return {"message": "Usuário cadastrado com sucesso."}, 201
        else:
            return {"message": "Ocorreu um erro, tente novamente"}, 500

    @jwt_required()
    def post(self):

        claims = get_jwt()
        print(claims)
        id_usuario = claims["id"]

        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = usuario_alteracao_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        duplicidade = UsuarioModel.busca_por_duplicidade(
            _email=dados["email"], _identidade=dados["identidade"], _id=id_usuario
        )

        if duplicidade:
            if duplicidade.identidade == dados["identidade"]:
                if len(dados["identidade"]) == 18:
                    return {"message": "CNPJ já cadastrado."}, 400
                else:
                    return {"message": "CPF já cadastrado."}, 400
            elif duplicidade.email == dados["email"]:
                return {"message": "Email já cadastrado."}, 400

        usuario = UsuarioModel.busca_por_id(_id=id_usuario)

        if usuario:
            for chave, valor in dados.items():
                setattr(usuario, chave, valor)

        if usuario.salva():
            return {"message": "Usuário alterado com sucesso."}, 200
        else:
            return {"message": "Ocorreu um erro, tente novamente"}, 500

    @jwt_required()
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        usuario = UsuarioModel.busca_por_email(_email=current_user)
        if usuario:
            usuario_json = AlteracaoUsuarioSchema(exclude=("password",))
            res = usuario_json.dump(usuario)
            return res, 200
        else:
            return {"message": "Usuário não localizado"}, 404
