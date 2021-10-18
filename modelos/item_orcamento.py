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

from db import Base, db_session
from modelos.base_model import ModeloBase, PaginacaoSchema


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
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    orcamento = relationship("OrcamentoModel", back_populates="itens_orcamento")

    def retorna_dicionario(self):
        dados = {}
        for c in self.__table__.columns:
            print(c.key, getattr(self, c.key))
            dados[c.key] = getattr(self, c.key)
        return dados

    @classmethod
    def busca_por_id_orcamento_e_id_usuario(cls, _id_usuario: int, _id_orcamento: int):
        """
        Realiza uma busca de Itens de um Orçamento com o id_orcamento e id_usuario
        SQL: id_orcamento = _id_orcamento AND id_usuario = _id_usuario
        :param _id_usuario: Filtro de usuário para limitar o acesso aos registros
        :param _id_orcamento: ID orçamento dos itens que serão buscados
        :return: Object Query
        """

        res = cls.query.filter(and_(cls.id_orcamento == _id_orcamento, cls.id_usuario == _id_usuario)).all()

        dados = {}
        dados["itens"] = (
            [item.retorna_dicionario() for item in res] if res else []
        )
        dados["total_registros"] = len(res)

        itens_orcamento_resultado_query_schema = ItemOrcamentoResultadoQuerySchema()

        return itens_orcamento_resultado_query_schema.dump(dados)

    @classmethod
    def busca_por_id_e_id_usuario(cls, _id_usuario: int, _id: int, _id_orcamento: int):
        """
        Busca por 'id' e 'id_usuario'
        SQL WHERE  id = {id} AND id_usuario = {id_usuario}
        :param _id_orcamento: Id do orçamento do item
        :param _id_usuario: Id do usuario para limitar a busca
        :param _id: Id do orçamento a ser buscado
        :return: Object Query
        """

        return cls.query.filter(
            and_(cls.id == _id, cls.id_usuario == _id_usuario, cls.id_orcamento == _id_orcamento)
        ).first()


class ItemOrcamentoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id_orcamento = fields.Integer(
        validate=validate.Range(min=1, error="ID orçamento inválido"),
        required=True,
        comment="ID orçamento",
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


class ItemOrcamentoIDSchema(ItemOrcamentoSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()


class ItemOrcamentoGetParamSchema(PaginacaoSchema):
    id_orcamento = fields.Integer(
        required=False,
        default=0,
        missing=0,
    )


class ItemOrcamentoResultadoQuerySchema(Schema):
    itens = fields.Nested(ItemOrcamentoIDSchema, missing=[], many=True)
    total_registros = fields.Integer(missing=0)