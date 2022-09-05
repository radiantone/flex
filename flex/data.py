import logging
from dataclasses import asdict, dataclass

import boto3
import botocore.exceptions

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s: "
    "%(levelname)s: "
    "%(funcName)s(): "
    "%(lineno)d:\t"
    "%(message)s",
)

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8009")


def persist_data(dataobject):
    schema = {
        "TableName": dataobject.__name__,
        "KeySchema": [
            {"AttributeName": dataobject.primary_key, "KeyType": "HASH"},
            {"AttributeName": dataobject.sort_key, "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": dataobject.primary_key, "AttributeType": "S"},
            {"AttributeName": dataobject.sort_key, "AttributeType": "N"},
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    }

    return schema


TYPES = {"str": "S", "int": "N"}


class class_or_instancemethod(classmethod):
    def __get__(self, instance, type_):
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)


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
        _dao = asdict(self)

        table = dynamodb.Table(self.__class__.__name__)

        table.put_item(Item=_dao)

    @class_or_instancemethod
    def delete(cls_or_self, *args, **kwargs):
        logging.info("Deleting %s %s %s", cls_or_self, args, kwargs)

        if isinstance(cls_or_self, type):
            logging.info("DELETE CLASS METHOD")
            table = cls_or_self.__name__
            fields = args[0]
        else:
            logging.info("DELETE INSTANCE METHOD")
            table = cls_or_self.__class__.__name__
            fields = {
                cls_or_self.primary_key: getattr(cls_or_self, cls_or_self.primary_key),
                cls_or_self.sort_key: getattr(cls_or_self, cls_or_self.sort_key),
            }

        where = ""
        params = []

        for field in fields:
            val = fields[field]
            if len(where) > 0:
                where += " AND "

            where += field + "=?"
            params += [val]

        sql = f"DELETE from {table} where {where}"
        logging.info("SQL %s %s", sql, params)
        return cls_or_self.execute(sql, params, response=True)

    @classmethod
    def find(cls, match, response=False):
        logging.debug("find")
        where = ""
        params = []

        for field in match:
            val = match[field]
            if len(where) > 0:
                where += " AND "

            where += field + "=?"
            params += [val]

        sql = f"SELECT * from {cls.__name__} where {where}"
        return cls.execute(sql, params, response=response)

    def relation(self, cls, backref=None, response=False):
        execute = getattr(cls, "execute")
        objects = execute(
            f'SELECT * FROM "{cls.__name__}" where {backref}=?',
            [self.id],
            response=response,
        )
        return objects

    @classmethod
    def execute(cls, statement, params, response=False):
        logging.debug("EXECUTE %s %s", statement, params)

        class ResultList:
            response = None

            def __init__(self, response):
                self.response = response

            def all(self):
                return [cls(**item) for item in self.response["Items"]]

            def first(self):
                return [cls(**item) for item in self.response["Items"]][0]

            def last(self):
                return [cls(**item) for item in self.response["Items"]][-1]

        try:
            output = dynamodb.meta.client.execute_statement(
                Statement=statement, Parameters=params
            )
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                logging.error(
                    "Couldn't execute PartiQL '%s' because the table does not exist.",
                    statement,
                )
            else:
                logging.error(
                    "Couldn't execute PartiQL '%s'. Here's why: %s: %s",
                    statement,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
            raise
        else:
            if response:
                return ResultList(output)
            else:
                return [cls(**item) for item in output["Items"]]  # ResultList(output)

    @classmethod
    def create_table(cls, skip_exists=False):

        _class = cls
        _schema = {}

        for name, val in _class.__dict__.items():
            if name.find("_") == 0:
                continue
            if val.__class__.__name__ in TYPES:
                _schema[name] = val

        for base in _class.__bases__:
            for name, val in base.__dict__.items():
                if name.find("_") == 0:
                    continue
                if val.__class__.__name__ in TYPES:
                    _schema[name] = val

        schema = persist_data(cls)

        try:
            table = dynamodb.create_table(**schema)
            table.wait_until_exists()
        except botocore.exceptions.ClientError as ex:
            if not skip_exists:
                raise ex

        return schema
