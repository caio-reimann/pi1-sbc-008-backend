from db import Base, db_session


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
