import re

from marshmallow import Schema, fields, validate, validates, ValidationError, EXCLUDE
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    or_,
    and_,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from bibliotecas.validacoes import valida_telefone, valida_cep
from db import Base
from modelos.base_model import ModeloBase


class OrcamentoModel(Base, ModeloBase):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, comment="ID")

    nome = Column(String(130), nullable=False, comment="Nome")
    email = Column(String(255), nullable=False, comment="Email")

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

    tel_celular = Column(String(20), nullable=False, comment="Celular")
    data_inicio = Column(DateTime, nullable=True, comment="Data de início")
    prazo = Column(Integer, nullable=True, comment="Prazo")
    tipo_prazo = Column(String(20), nullable=True, comment="Tipo prazo")
    info_complementar = Column(Text, comment="Informações complementares")

    id_usuario = Column(
        Integer,
        ForeignKey(
            "usuarios.id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    usuario = relationship("UsuarioModel", back_populates="clientes")

    @classmethod
    def busca_por_email(cls, _email: str):
        """
        Busca por 'email' WHERE  email = {_email}
        :param _email: Id a ser buscado
        :return: Object Query
        """
        return cls.query.filter_by(email=_email).first()

    @classmethod
    def busca_por_duplicidade(cls, _identidade: str, _id_usuario: str, _id: int = 0):
        if _id > 0:
            return cls.query.filter(
                and_(
                    cls.id != _id,
                    cls.identidade == _identidade,
                    cls.id_usuario == _id_usuario,
                )
            ).first()
        else:
            return cls.query.filter(
                and_(cls.identidade == _identidade, cls.id_usuario == _id_usuario)
            ).first()


class CadastramentoUsuarioSchema(Schema):
    class Meta:
        unknown = EXCLUDE

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
    identidade = fields.Str(
        required=True, error_messages={"required": "O campo 'CPF/CNPJ' é obrigatório"}
    )
    email = fields.Str(
        required=True,
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )
    tel_celular = fields.Str(validate=valida_telefone)
    info_complementar = fields.Str(
        validate=validate.Length(
            max=300,
            error="O campo 'Descrição' deve ter no máximo 300 caracteres.",
        ),
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
