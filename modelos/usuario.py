import re

from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError,
    EXCLUDE,
    validates_schema,
)
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, or_, and_
from sqlalchemy.orm import relationship

from bibliotecas.validacoes import valida_telefone, valida_cep
from db import Base
from modelos.base_model import ModeloBase


class UsuarioModel(Base, ModeloBase):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, comment="ID")
    email = Column(String(255), unique=True, nullable=False, comment="Email")
    password = Column(String(255), nullable=False, comment="Senha")
    active = Column(Boolean(), comment="Ativo")

    nome = Column(String(30), nullable=False, comment="Nome")
    sobrenome = Column(String(100), unique=False, nullable=False, comment="Sobrenome")
    sexo = Column(String(15), unique=False, nullable=False, comment="Sexo")
    identidade = Column(String(30), unique=True, nullable=False, comment="CPF|CNPJ")
    profissao = Column(String(100), nullable=False, comment="Profissão")
    tel_celular = Column(String(20), nullable=True, comment="Celular")
    tel_comercial = Column(String(20), nullable=True, comment="Telefone comercial")
    tel_comercial2 = Column(String(20), nullable=True, comment="Telefone comercial2")
    tel_comercial3 = Column(String(20), nullable=True, comment="Telefone comercial3")
    logradouro = Column(String(150), nullable=True, comment="Endereço")
    numero = Column(String(20), nullable=True, comment="Número")
    complemento = Column(String(50), nullable=True, comment="Complemento")
    bairro = Column(String(100), nullable=True, comment="Bairro")
    cidade = Column(String(100), nullable=True, comment="Cidade")
    uf = Column(String(2), nullable=True, comment="Estado")
    cep = Column(String(10), nullable=True, comment="CEP")
    info_complementar = Column(Text, comment="Informações complementares")

    orcamentos = relationship("OrcamentoModel", back_populates="usuario")
    itens_orcamento = relationship("ItemOrcamentoModel", back_populates="usuario")

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

    @classmethod
    def busca_por_duplicidade(cls, _identidade: str, _email: str, _id: int = 0):
        if _id > 0:
            return cls.query.filter(
                or_(cls.identidade == _identidade) | (cls.email == _email),
                and_(cls.id != _id),
            ).first()
        else:
            return cls.query.filter(
                (cls.identidade == _identidade) | (cls.email == _email)
            ).first()


class AutenticacaoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    email = fields.Str(
        required=True,
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )
    password = fields.Str(
        required=True, error_messages={"required": "O campo 'Senha' é obrigatório"}
    )


class SenhaUsuarioSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=6,
            max=30,
            error="O campo 'Senha' deve ter no mínimo 6 e no máximo 30 caracteres.",
        ),
        error_messages={"required": "O campo 'Senha' é obrigatório"},
    )
    cpassword = fields.Str(
        required=True,
        error_messages={"required": "O campo 'Confirmar senha' é obrigatório"},
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["password"] != data["cpassword"]:
            raise ValidationError(
                "O campo 'Senha' e 'Confirmar senha' devem ser iguais."
            )


class CadastramentoUsuarioSchema(SenhaUsuarioSchema):
    class Meta:
        unknown = EXCLUDE

    email = fields.Str(
        required=True,
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=6,
            max=30,
            error="O campo 'Senha' deve ter no mínimo 6 e no máximo 30 caracteres.",
        ),
        error_messages={"required": "O campo 'Senha' é obrigatório"},
    )
    cpassword = fields.Str(
        required=True,
        error_messages={"required": "O campo 'Confirmar senha' é obrigatório"},
    )
    nome = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=30,
            error="O campo 'Nome' deve ter no mínimo 2 e no máximo 30 caracteres.",
        ),
        error_messages={"required": "O campo 'Nome' é obrigatório"},
    )
    sobrenome = fields.Str(
        required=True,
        validate=validate.Length(
            min=6,
            max=100,
            error="O campo 'Sobrenome' deve ter no mínimo 6 e no máximo 100 caracteres.",
        ),
        error_messages={"required": "O campo 'Sobrenome' é obrigatório"},
    )
    sexo = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=["M", "F", "O"], error="Opção inválida para o campo 'Sexo'."
        ),
        error_messages={"required": "O campo 'Sexo' é obrigatório"},
    )
    identidade = fields.Str(
        required=True, error_messages={"required": "O campo 'CPF/CNPJ' é obrigatório"}
    )
    profissao = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error="O campo 'Profissão' deve ter no mínimo 2 e no máximo 100 caracteres.",
        ),
        error_messages={"required": "O campo 'Profissão' é obrigatório"},
    )
    aceite_termo = fields.Boolean(
        required=True,
        error_messages={"required": "O campo 'Aceito termo' é obrigatório"},
    )

    @validates("identidade")
    def valida_cpf_cnpj(self, value):
        from validate_docbr import CPF, CNPJ

        if len(value) == 18:
            cnpj = CNPJ()
            if cnpj.validate(value) is False:
                raise ValidationError("'CNPJ' inválido.")
        else:
            cpf = CPF()
            if cpf.validate(value) is False:
                raise ValidationError("'CPF' inválido.")


class AlteracaoUsuarioSchema(CadastramentoUsuarioSchema):
    class Meta:
        unknown = EXCLUDE
        exclude = ("password", "cpassword", "aceite_termo")

    tel_celular = fields.Str(validate=valida_telefone)
    tel_comercial = fields.Str(validate=valida_telefone)
    tel_comercial2 = fields.Str(validate=valida_telefone)
    tel_comercial3 = fields.Str(validate=valida_telefone)
    logradouro = fields.Str(
        validate=validate.Length(
            max=150,
            error="O campo 'Logradouro' deve ter no máximo 150 caracteres.",
        ),
    )
    numero = fields.Str(
        validate=validate.Length(
            max=20,
            error="O campo 'Número' deve ter no máximo 20 caracteres.",
        ),
    )
    complemento = fields.Str(
        validate=validate.Length(
            max=50,
            error="O campo 'Complemento' deve ter no máximo 50 caracteres.",
        ),
    )
    bairro = fields.Str(
        validate=validate.Length(
            max=100,
            error="O campo 'Bairro' deve ter no máximo 100 caracteres.",
        ),
    )
    cidade = fields.Str(
        validate=validate.Length(
            max=100,
            error="O campo 'Cidade' deve ter no máximo 100 caracteres.",
        ),
    )
    uf = fields.Str(
        validate=validate.OneOf(
            [
                "AC",
                "AL",
                "AP",
                "AM",
                "BA",
                "CE",
                "DF",
                "ES",
                "GO",
                "MA",
                "MT",
                "MS",
                "MG",
                "PA",
                "PB",
                "PR",
                "PE",
                "PI",
                "RJ",
                "RN",
                "RS",
                "RO",
                "RR",
                "SC",
                "SP",
                "SE",
                "TO",
            ],
            error="Campo 'Estado': opção de  inválida",
        ),
    )
    cep = fields.Str(validate=valida_cep)

    info_complementar = fields.Str(
        validate=validate.Length(
            max=300,
            error="O campo 'Descrição' deve ter no máximo 300 caracteres.",
        ),
    )

    @validates_schema
    def validate_schema(self, data, **kwargs):
        pass


class VisualizacaoUsuarioSchema(AlteracaoUsuarioSchema):
    class Meta:
        exclude = ("password", "cpassword")


class RecuperaSenhaEmailUsuarioSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    email = fields.Str(
        required=True,
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )
