from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from marshmallow import ValidationError

from modelos.usuario import AutenticacaoModel, UsuarioModel

auth_schema = AutenticacaoModel()


class Autenticacao(Resource):
    """ """
    def post(self):
        json_dados = request.get_json()
        if not json_dados:
            return {"message": "Nenhum dado foi enviado"}, 400

        try:
            dados = auth_schema.load(json_dados)
        except ValidationError as err:
            return err.messages, 422

        usuario = UsuarioModel.busca_por_email(_email=dados['email'])

        if usuario:
            from app import bcrypt

            if bcrypt.check_password_hash(usuario.password, dados['password']):
                access_token = create_access_token(identity=dados['email'])
                return jsonify(access_token=access_token)
            else:
                return {'message': 'Email ou senha inválido(s)'},  400
        else:
            return {'message': 'Usuário não encontrado'}, 404

    def get(self):
        return "OK", 200


class AtualizacaoToken(Resource):
    def post(self):
        return "OK", 200
