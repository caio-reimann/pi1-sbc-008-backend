from marshmallow import Schema, INCLUDE, fields, EXCLUDE
from sqlalchemy import and_

from db import Base, db_session


class OrdemCustomizada:
    """
    Ordem para a query do Crud
    :param coluna: Coluna da tabela que será filtrada
    :param tipo: 'C' Crescente (ASC) ou 'D' Decrescente (DESC)
    """

    def __init__(self, coluna: str, tipo: str):
        self.coluna = coluna
        self.tipo = ""
        if tipo == "C" or tipo == "D":
            self.tipo = tipo
        else:
            raise ValueError("O parâmetro 'tipo' deve ter o valor 'C' ou 'D'")

    def __del__(self):
        pass

    def gera_texto(self):
        if self.tipo == "C":
            return "{} {}".format(self.coluna, "asc")
        if self.tipo == "D":
            return "{} {}".format(self.coluna, "desc")


class FiltroCustomizado:
    """
    Filtro para a query do crud
    :param coluna: Coluna da tabela que será filtrada
    :param tipo: método de filtro utilizado '==', "!=", '<>', 'in' ou 'like'
    :param valor: Valor utilizado no filtro (no caso 'contem', incluir o % antes e ou depois)
    """

    def __init__(self, coluna: str, tipo: str, valor):
        self.coluna = coluna
        self.valor = valor
        self.tipo = ""
        if (
            tipo == "!="
            or tipo == "=="
            or tipo == "like"
            or tipo == "<>"
            or tipo == "in"
        ):
            self.tipo = tipo
        else:
            raise ValueError("O parâmetro 'tipo' deve ter o valor '==', '<>', ou 'like")

    def __del__(self):
        pass


class ModeloBase:
    @classmethod
    def busca_por_id(cls, _id: int):
        """
        Busca por 'id' WHERE  id = {id}
        :param _id: Id a ser buscado
        :return: Object Query
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def compara_variaveis(cls, var1, var2):
        """
        Compara duas variáveis ({var1} e {var2}) e retorna:
        True - Se forem iguais;
        False - Se forem diferentes.
        :param var1: Variável 1
        :param var2: Variável 2
        :return:
        """
        if len(var1) != len(var2):
            return False

        for c1, c2 in zip(var1, var2):
            if c1 != c2:
                return False
        return True

    def salva(self) -> bool:
        """
        Salva o registro no Banco de dados
        :return: True se deu certo, False se algo deu errado
        """
        from sqlalchemy.exc import DBAPIError

        try:
            db_session.add(self)
            db_session.commit()
            return True

        except DBAPIError as error:
            print(error)
            db_session.rollback()
            return False

        except Exception as e:
            print(e)
            return False

    @classmethod
    def remove_por_id_e_id_usuario(cls, _id_usuario: int, _id: int):
        """
        Busca por 'id' e 'id_usuario' e remove o registro
        SQL WHERE  id = {id} AND id_usuario = {id_usuario}
        :param _id_usuario: Id do usuario para limitar a busca
        :param _id: Id do registro a ser buscado
        :return: Object Query
        """
        try:
            registro = cls.query.filter(
                and_(cls.id == _id, cls.id_usuario == _id_usuario)
            ).delete()
            db_session.commit()
            if registro == 1:
                return True
            else:
                return None
        except Exception as e:
            return e

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}




class PaginacaoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    pagina = fields.Integer(
        required=False,
        default=1,
        missing=1,
    )
    limite = fields.Integer(
        required=False,
        default=10,
        missing=10,
    )


class ResultadoQuerySchema(PaginacaoSchema):
    total_registros = fields.Integer(
        required=False,
        default=1,
        missing=1,
    )
    total_paginas = fields.Integer(
        required=False,
        default=1,
        missing=1,
    )
