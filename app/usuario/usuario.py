from datetime import datetime

from pydantic import Field

from nordic_realm.mongo import MongoBaseModel
from nordic_realm.utils.pydantic.types import DateTimeNowExcluded


class Usuario(MongoBaseModel[str]):
    nome: str
    sobrenome: str

    email: str
    senha: str = Field(exclude=True)

    dt_criacao: datetime = DateTimeNowExcluded
    dt_ultima_edicao: datetime = DateTimeNowExcluded

    def full_name(self) -> str:
        return f"{self.nome} {self.sobrenome}"
