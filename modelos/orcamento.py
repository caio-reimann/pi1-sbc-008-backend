import datetime
import math
from typing import List

from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError,
    EXCLUDE,
    validates_schema,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    or_,
    and_,
    ForeignKey,
    BigInteger,
    text,
)
from sqlalchemy.orm import relationship, load_only

from bibliotecas.validacoes import valida_telefone, valida_cep
from db import Base
from modelos.base_model import (
    ModeloBase,
    OrdemCustomizada,
    PaginacaoSchema,
    ResultadoQuerySchema,
)


class OrcamentoModel(Base, ModeloBase):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, comment="ID")

    nome = Column(String(130), nullable=False, comment="Nome")
    email = Column(String(255), comment="Email")
    identidade = Column(String(30), comment="CPF|CNPJ")

    logradouro = Column(String(150), nullable=True, comment="Endereço")
    numero = Column(String(20), nullable=True, comment="Número")
    complemento = Column(String(50), nullable=True, comment="Complemento")
    bairro = Column(String(100), nullable=True, comment="Bairro")
    cidade = Column(String(100), nullable=True, comment="Cidade")
    uf = Column(String(2), nullable=True, comment="Estado")
    cep = Column(String(10), nullable=True, comment="CEP")

    tel_celular = Column(String(20), nullable=False, comment="Celular")

    data_criacao = Column(
        DateTime,
        nullable=True,
        comment="Data de início",
        default=datetime.datetime.now(),
    )

    # Prazos para o término
    data_inicio = Column(DateTime, nullable=True, comment="Data de início")
    prazo = Column(Integer, nullable=True, comment="Prazo")
    tipo_prazo = Column(String(20), nullable=True, comment="Tipo prazo")

    # Informações gerais sobre o orçamento
    descricao = Column(Text, comment="Descrição")
    info_complementar = Column(Text, comment="Informações complementares")

    desconto = Column(BigInteger, default=0, comment="Desconto em valor")
    desconto_porcentagem = Column(Integer, default=0, comment="Desconto em %")

    id_usuario = Column(
        Integer,
        ForeignKey(
            "usuarios.id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    usuario = relationship("UsuarioModel", back_populates="orcamentos")

    itens_orcamento = relationship("ItemOrcamentoModel", back_populates="orcamento")

    @classmethod
    def busca_por_id_e_usuario(cls, _id_usuario: int, _id: int):
        """
        Busca por 'id' WHERE  id = {id}
        :param _id_usuario: Id do usuario
        :param _id: Id a ser buscado
        :return: Object Query
        """

        res = cls.query.filter(
            and_(cls.id == _id, cls.id_usuario == _id_usuario)
        ).first()

        orcamento_visualizacao_schema = OrcamentoVisualizacaoSchema()

        return orcamento_visualizacao_schema.dump(res) if res else None

    @classmethod
    def busca_por_nome_ou_identidade(
        cls,
        _id_usuario,
        _limite: int = 10,
        _nome: str = None,
        _identidade: str = None,
        _pagina: int = 1,
        _ordenacoes: List[OrdemCustomizada] = [],
    ):
        """
        Realiza uma busca de Orçamentos com o nome ou identidade, e id_usuario
        SQL: (nome LIKE(%_nome%) OR identidade LIKE(%_identidade%))  AND id_usuario = _id_usuario
        :param _id_usuario: Filtro de usuário para limitar o acesso aos registros
        :param _pagina: Página selecionada para trazer os resultados
        :param _limite: Quantidade de registros que será selecionados por vez (máximo 20)
        :param _identidade: Identidade que será buscada utilizado a expressão SQL LIKE %valor%
        :param _nome: Nome que será buscado utilizado a expressão SQL LIKE %valor%
        :param _ordenacoes: Adiciona as ordenações no comando SQL
        :return: Object Query
        """

        if _pagina <= 0:
            _pagina = 1
        if _limite > 30 or _limite <= 0:
            _limite = 10

        _query = cls.query

        if _nome:
            if _identidade:
                _query = _query.filter(
                    (
                        and_(
                            or_(
                                cls.nome.ilike(f"%{_nome}%"),
                                cls.identidade.ilike(f"%{_identidade}%"),
                            ),
                            cls.id_usuario == _id_usuario,
                        )
                    )
                )
            else:
                _query = _query.filter(
                    and_(
                        cls.nome.ilike(f"%{_nome}%"),
                        cls.id_usuario == _id_usuario,
                    )
                )
        elif _identidade:
            _query = _query.filter(
                and_(
                    cls.identidade.ilike(f"%{_identidade}%"),
                    cls.id_usuario == _id_usuario,
                )
            )

        _total_registros = _query.options(load_only(cls.id)).count()

        _query_ordenacoes = []
        for ordenacao in _ordenacoes:
            _query_ordenacoes.append(ordenacao.gera_texto())

        if len(_query_ordenacoes) > 0:
            _query = _query.order_by(text(",".join(_query_ordenacoes)))

        res = _query.limit(_limite).offset(
            ((_pagina - 1) * _limite) if _pagina > 1 else 0
        ).all()

        dados = {}
        dados["orcamentos"] = (
            [_orcamento.retorna_dicionario() for _orcamento in res] if res else []
        )
        dados["total_registros"] = _total_registros
        dados["total_paginas"] = math.ceil(_total_registros / _limite)
        dados["pagina"] = _pagina
        dados["limite"] = _limite

        orcamento_resultado_query_schema = OrcamentoResultadoQuerySchema()

        return orcamento_resultado_query_schema.dump(dados)

    def retorna_dicionario(self):
        dados = {}
        for c in self.__table__.columns:
            print(c.key, getattr(self, c.key))
            dados[c.key] = getattr(self, c.key)
        return dados


class OrcamentoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nome = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=130,
            error="O campo 'Nome' deve ter no mínimo 2 e no máximo 130 caracteres.",
        ),
        error_messages={"required": "O campo 'Nome' é obrigatório"},
    )

    identidade = fields.Str()

    email = fields.Str(
        required=False,
        default=None,
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )

    tel_celular = fields.Str(default=None, validate=valida_telefone)

    logradouro = fields.Str(
        default=None,
        validate=validate.Length(
            max=150,
            error="O campo 'Logradouro' deve ter no máximo 150 caracteres.",
        ),
    )
    numero = fields.Str(
        default=None,
        validate=validate.Length(
            max=20,
            error="O campo 'Número' deve ter no máximo 20 caracteres.",
        ),
    )
    complemento = fields.Str(
        default=None,
        validate=validate.Length(
            max=50,
            error="O campo 'Complemento' deve ter no máximo 50 caracteres.",
        ),
    )
    bairro = fields.Str(
        default=None,
        validate=validate.Length(
            max=100,
            error="O campo 'Bairro' deve ter no máximo 100 caracteres.",
        ),
    )
    cidade = fields.Str(
        default=None,
        validate=validate.Length(
            max=100,
            error="O campo 'Cidade' deve ter no máximo 100 caracteres.",
        ),
    )
    uf = fields.Str(
        default=None,
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
    cep = fields.Str(default=None, validate=valida_cep)

    data_inicio = fields.DateTime(
        required=True,
        comment="Data de início",
        error_messages={"required": "O campo 'Data inínio' é obrigatório"},
    )
    tipo_prazo = fields.String(
        default=None,
        validate=validate.OneOf(
            ["Horas", "Dias", "Meses"],
            error="O Campo 'Tipo do prazo' deve ser: Horas, Dias ou Meses",
        ),
        comment="Tipo prazo",
    )
    prazo = fields.Integer(
        default=None,
        validate=validate.Range(min=1, error="O campo 'Prazo' deve ser maior que 0"),
        comment="Prazo",
    )

    descricao = fields.Str(
        default=None,
        validate=validate.Length(
            max=300,
            error="O campo 'Descrição' deve ter no máximo 300 caracteres.",
        ),
    )

    info_complementar = fields.Str(
        default=None,
        validate=validate.Length(
            max=300,
            error="O campo 'Informações complementares' deve ter no máximo 300 caracteres.",
        ),
    )

    desconto = fields.Integer(
        validate=validate.Range(
            min=0, error="O campo 'Desconto' não pode ser menor que 0"
        ),
        default=0,
        comment="Desconto",
    )

    desconto_porcentagem = fields.Integer(
        validate=validate.Range(
            min=0, error="O campo 'Desconto em %' não pode ser menor que 0"
        ),
        default=0,
        comment="Desconto em %",
    )

    @validates("identidade")
    def valida_cpf_cnpj(self, value):
        if value is not None and value != "":
            from validate_docbr import CPF, CNPJ

            if len(value) == 18:
                cnpj = CNPJ()
                if cnpj.validate(value) is False:
                    raise ValidationError("'CNPJ' inválido.")
            else:
                cpf = CPF()
                if cpf.validate(value) is False:
                    raise ValidationError("'CPF' inválido.")

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["desconto"] > 0 and data["desconto_porcentagem"] > 0:
            raise ValidationError(
                "Preencha apenas um dos campos: 'Desconto' ou 'Desconto em %'"
            )


class OrcamentoVisualizacaoSchema(OrcamentoSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer()
    data_criacao = fields.DateTime()


class OrcamentoGetParamSchema(PaginacaoSchema):
    id = fields.Integer(
        required=False,
        default=0,
        missing=0,
    )
    nome = fields.String(
        required=False,
        default=None,
        missing=None,
    )
    identidade = fields.String(
        required=False,
        default=None,
        missing=None,
    )


class OrcamentoResultadoQuerySchema(ResultadoQuerySchema):
    orcamentos = fields.Nested(OrcamentoVisualizacaoSchema, missing=[], many=True)
