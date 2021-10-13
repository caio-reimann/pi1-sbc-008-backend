import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import ReturnTypeFromArgs

from dotenv import load_dotenv

# Load all environments variables
load_dotenv()

engine = create_engine(
    os.environ.get("DATABASE_URL"),
    pool_size=int(os.environ.get("DB_POOL_SIZE")),
    max_overflow=int(os.environ.get("DB_MAX_OVERFLOW")),
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=True if os.environ.get("DEBUG_SQL") == "1" else False,
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db(bcrypt):
    # Importar todos os modelos para criá-los automaticamente
    from modelos.usuario import UsuarioModel
    from modelos.clientes import ClienteModel

    if os.getenv("DB_INIT") == "1":
        Base.metadata.create_all(bind=engine)

    if os.getenv("DB_CREATE_ADMIN") == "1":
        usuario = UsuarioModel()
        usuario.nome = "Admin"
        usuario.sobrenome = "Administrador"
        usuario.email = os.environ.get("DB_ADMIN_EMAIL")
        usuario.password = bcrypt.generate_password_hash(
            os.environ.get("DB_ADMIN_PASSWORD")
        ).decode("utf-8")
        usuario.active = True
        usuario.aceite_termo = True
        usuario.identidade = "000.000.000-00"
        usuario.profissao = "Administrador"
        usuario.sexo = "M"

        if usuario.salva():
            print("Administrador cadastrado com sucesso")


class unaccent(ReturnTypeFromArgs):
    pass
