import logging
from dataclasses import asdict, dataclass
from flex.backends import FlexBackendFactory


logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s: "
    "%(levelname)s: "
    "%(funcName)s(): "
    "%(lineno)d:\t"
    "%(message)s",
)


class class_or_instancemethod(classmethod):
    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)


backend = FlexBackendFactory.get()


@dataclass
class DataclassBase:
    name: str = "None"
    id: str = "inv1"

    @classmethod
    @property
    def primary_key(cls) -> str:
        return "id"

    @classmethod
    @property
    def sort_key(cls) -> str:
        return "name"

    def save(self):
        return backend.save(self)

    @class_or_instancemethod
    def delete(cls_or_self, *args, **kwargs):
        return backend.delete(cls_or_self, *args, **kwargs)

    @classmethod
    def find(cls, match, response=False):
        return backend.find(cls, match, response=response)

    def relation(self, cls, backref=None, response=False):
        return backend.relation(self, cls, backref=backref, response=response)

    @classmethod
    def execute(cls, statement, params, response=False):
        return backend.execute(cls, statement, params, response=response)

    @classmethod
    def create_table(cls, skip_exists=False):
        return backend.create_table(cls, skip_exists=skip_exists)
