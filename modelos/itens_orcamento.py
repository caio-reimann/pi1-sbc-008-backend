from marshmallow import Schema, fields, validate, EXCLUDE
from sqlalchemy import (
    Column,
    Integer,
    String,
    and_,
    ForeignKey,
    BigInteger,
)
from sqlalchemy.orm import relationship

from db import Base
from modelos.base_model import ModeloBase


class ItemOrcamentoModel(Base, ModeloBase):
    __tablename__ = "itens_orcamento"

    id = Column(Integer, primary_key=True, comment="ID")
    descricao = Column(String(130), nullable=False, comment="Nome")
    quantidade = Column(Integer, nullable=False, comment="Quantidade")
    valor = Column(BigInteger, nullable=False, comment="Valor unitário")

    id_usuario = Column(
        Integer,
        ForeignKey(
            "usuarios.id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    usuario = relationship("UsuarioModel", back_populates="itens_orcamento")

    id_orcamento = Column(
        Integer,
        ForeignKey(
            "orcamentos.id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    orcamento = relationship("OrcamentoModel", back_populates="itens_orcamento")

    @classmethod
    def busca_por_orcamento(
        cls, _id_usuario: int, _id_orcamento: int, _limit: int, _page: int = 1
    ):
        """
        Realiza uma busca de Orçamentos com o id_orcamento e id_usuario
        SQL: id_orcamento = _id_orcamento AND id_usuario = _id_usuario
        :param _id_usuario: Filtro de usuário para limitar o acesso aos registros
        :param _page: Página selecionada para trazer os resultados
        :param _limit: Quantidade de registros que será selecionados por vez (máximo 20)
        :param _id_orcamento: ID orçamento que será buscado
        :return: Object Query
        """

        if _page < 0:
            _page = 1

        return cls.query.filter(
            and_(cls.nome.ilike(f"%{_id_orcamento}%", cls.id_usuario == _id_usuario))
            .limit(_limit)
            .offset((_page * _limit))
        )


class CadastramentoItemOrcamentoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id_orcamento = fields.Integer(
        validate=validate.Range(min=1, error="ID orçamento inválido"),
        required=True,
        comment="ID orçamento",
    )

    _id_usuario = fields.Integer(
        validate=validate.Range(min=1, error="ID usuário inválido"),
        required=True,
        comment="ID usuário",
    )

    descricao = fields.Str(
        validate=validate.Length(
            max=130,
            error="O campo 'Descrição' deve ter no máximo 130 caracteres.",
        ),
        required=True,
        error_messages={"required": "O campo 'Descrição' é obrigatório"},
        comment="Descrição",
    )

    quantidade = fields.Integer(
        validate=validate.Range(
            min=1, error="O campo 'Quantidade' não pode ser menor que 1"
        ),
        required=True,
        error_messages={"required": "O campo 'Quantidade' é obrigatório"},
        comment="Quantidade",
    )

    valor = fields.Integer(
        validate=validate.Range(
            min=0, error="O campo 'Valor' não pode ser menor que 0"
        ),
        required=True,
        default=0,
        error_messages={"required": "O campo 'Valor' é obrigatório"},
        comment="Valor",
    )
