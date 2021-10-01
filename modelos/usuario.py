from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text

from db import Base
from modelos.base_model import ModeloBase


class UsuarioModel(Base, ModeloBase):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, comment="ID")
    email = Column(String(255), unique=True, nullable=False, comment="Email")
    password = Column(String(255), nullable=False, comment="Senha")
    active = Column(Boolean(), comment="Ativo")

    nome = Column(String(255), nullable=False, comment="Nome")
    sobrenome = Column(String(255), unique=False, nullable=False, comment="Sobrenome")
    identidade = Column(String(30), unique=True, nullable=False, comment="CPF|CNPJ")
    profissao = Column(String(100), nullable=False, comment="Profissão")
    tel_celular = Column(String(100), nullable=True, comment="Celular")
    tel_comercial = Column(String(100), nullable=True, comment="Telefone comercial")
    tel_comercial2 = Column(String(100), nullable=True, comment="Telefone comercial2")
    tel_comercial3 = Column(String(100), nullable=True, comment="Telefone comercial3")
    logradouro = Column(String(100), nullable=True, comment="Endereço")
    numero = Column(String(100), nullable=True, comment="Número")
    complemento = Column(String(100), nullable=True, comment="Complemento")
    bairro = Column(String(100), nullable=True, comment="Bairro")
    cidade = Column(String(100), nullable=True, comment="Cidade")
    uf = Column(String(2), nullable=True, comment="Estado")
    cep = Column(String(100), nullable=True, comment="CEP")
    info_complementar = Column(Text, comment="Informações complementares")

    aceite_termo = Column(
        Boolean,
        nullable=False,
        comment="Aceitou Termo",
    )

    @classmethod
    def busca_por_email(cls, _email: str):
        """
        Busca por 'email' WHERE  email = {_email}
        :param _email: Id a ser buscado
        :return: Object Query
        """
        return cls.query.filter_by(email=_email).first()


class AutenticacaoModel(Schema):
    email = fields.Str(
        required=True,
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "O campo 'Senha' é obrigatório"}
    )
