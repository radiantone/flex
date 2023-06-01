import logging
import warnings

from pydantic.dataclasses import dataclass

from flex.backends import FlexBackendFactory

warnings.filterwarnings("ignore")
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
class FlexObject:
    from datetime import datetime

    curr_dt = datetime.now()

    timestamp = int(round(curr_dt.timestamp()))

    id: str = "inv1"
    name: str = "None"

    timestamp: int = timestamp
    updated: int = timestamp

    @classmethod
    @property
    def primary_key(cls) -> str:
        return "id"

    @classmethod
    @property
    def sort_key(cls) -> str:
        return "timestamp"

    def save(self, create_table=True):
        self.__class__.create_table(skip_exists=True)
        return backend.save(self)

    def fields(self):
        return [
            d
            for d in dir(self)
            if d.find("_") != 0
            and (
                type(getattr(self, d)) == str
                or type(getattr(self, d)) == int
                or type(getattr(self, d)) == dict
            )
        ]

    @class_or_instancemethod
    def delete(cls, *args, **kwargs):
        return backend.delete(cls, *args, **kwargs)

    @classmethod
    def find(cls, match, response=False):
        return backend.find(cls, match, response=response)

    def relation(self, cls, backref=None, response=False):
        return backend.relation(self, cls, backref=backref, response=response)

    @classmethod
    def execute(
        cls,
        statement,
        params,
        response=False,
        consistentread=True,
        nexttoken=None,
        returnconsumedcapacity="NONE",
        limit=1,
    ):

        kwargs = {
            "consistentread": consistentread,
            "returnconsumedcapacity": returnconsumedcapacity,
            "limit": limit,
        }
        if nexttoken:
            kwargs["nexttoken"] = nexttoken

        return backend.execute(cls, statement, params, response=response, **kwargs)

    @classmethod
    def create_table(cls, skip_exists=False):
        return backend.create_table(cls, skip_exists=skip_exists)
