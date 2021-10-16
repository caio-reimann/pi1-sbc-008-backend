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
)
from sqlalchemy.orm import relationship

from bibliotecas.validacoes import valida_telefone, valida_cep
from db import Base
from modelos.base_model import ModeloBase


class OrcamentoModel(Base, ModeloBase):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, comment="ID")

    nome = Column(String(130), nullable=False, comment="Nome")
    email = Column(String(255), comment="Email")
    identidade = Column(String(30), comment="CPF|CNPJ")

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
    def busca_por_nome(cls, _id_usuario, _nome: str, _limit: int, _page: int = 1):
        """
        Realiza uma busca de Orçamentos com o nome e id_usuario
        SQL: nome LIKE(%_nome%) AND id_usuario = _id_usuario
        :param _id_usuario: Filtro de usuário para limitar o acesso aos registros
        :param _page: Página selecionada para trazer os resultados
        :param _limit: Quantidade de registros que será selecionados por vez (máximo 20)
        :param _nome: Nome que será buscado utilizado a expressão SQL LIKE %valor%
        :return: Object Query
        """

        if _page < 0:
            _page = 1

        return cls.query.filter(
            and_(cls.nome.ilike(f"%{_nome}%", cls.id_usuario == _id_usuario))
            .limit(_limit)
            .offset((_page * _limit))
        )

    @classmethod
    def busca_por_nome_ou_identidade(
        cls,
        _id_usuario,
        _limit: int = 10,
        _nome: str = "",
        _identidade: str = "",
        _page: int = 1,
    ):
        """
        Realiza uma busca de Orçamentos com o nome ou identidade, e id_usuario
        SQL: (nome LIKE(%_nome%) OR identidade LIKE(%_identidade%))  AND id_usuario = _id_usuario
        :param _id_usuario: Filtro de usuário para limitar o acesso aos registros
        :param _page: Página selecionada para trazer os resultados
        :param _limit: Quantidade de registros que será selecionados por vez (máximo 20)
        :param _identidade: Identidade que será buscada utilizado a expressão SQL LIKE %valor%
        :param _nome: Nome que será buscado utilizado a expressão SQL LIKE %valor%
        :return: Object Query
        """

        if _page < 0:
            _page = 1
        if _limit > 20 or _limit < 0:
            _limit = 20

        return cls.query.filter(
            (
                and_(
                    or_(
                        cls.nome.ilike(f"%{_nome}%"),
                        cls.identidade.ilike(f"%{_identidade}%"),
                    ),
                    cls.id_usuario == _id_usuario,
                )
            )
            .limit(_limit)
            .offset((_page * _limit))
        )


class CadastramentoOrcamentoSchema(Schema):
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
        validate=validate.Email(error="Email inválido"),
        error_messages={"required": "O campo 'Email' é obrigatório"},
    )

    tel_celular = fields.Str(validate=valida_telefone)

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

    data_inicio = fields.DateTime(
        required=True,
        comment="Data de início",
        error_messages={"required": "O campo 'Data inínio' é obrigatório"},
    )
    tipo_prazo = fields.String(
        validate=validate.OneOf(
            ["Horas", "Dias", "Meses"],
            error="O Campo 'Tipo do prazo' deve ser: Horas, Dias ou Meses",
        ),
        comment="Tipo prazo",
    )
    prazo = fields.Integer(
        validate=validate.Range(min=1, error="O campo 'Prazo' deve ser maior que 0"),
        comment="Prazo",
    )

    descricao = fields.Str(
        validate=validate.Length(
            max=300,
            error="O campo 'Descrição' deve ter no máximo 300 caracteres.",
        ),
    )

    info_complementar = fields.Str(
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
