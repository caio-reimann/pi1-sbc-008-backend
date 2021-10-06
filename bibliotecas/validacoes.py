import re

from marshmallow import ValidationError


def valida_telefone(value: str):
    if len(value) > 0:
        if (
            re.fullmatch("^[(]{1}[0-9]{2}[)]{1} [0-9]{4,5}[-]{1}[0-9]{4}$", value)
            is None
        ):
            raise ValidationError("Celular inválido.")


def valida_cep(value: str):
    if len(value) > 0:
        if re.fullmatch("^[0-9]{5}-[0-9]{3}$", value) is None:
            raise ValidationError("CEP inválido.")
