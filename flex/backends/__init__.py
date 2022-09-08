import logging
import os
from abc import ABC, abstractmethod
from dataclasses import asdict

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s: "
    "%(levelname)s: "
    "%(funcName)s(): "
    "%(lineno)d:\t"
    "%(message)s",
)


class FlexBackend(ABC):
    @abstractmethod
    def save(self, dataobject):
        ...

    @abstractmethod
    def delete(self, cls_or_self, *args, **kwargs):
        ...

    @abstractmethod
    def find(self, cls, match, response=False):
        ...

    @abstractmethod
    def relation(self, cls, backref=None, response=False):
        ...

    @abstractmethod
    def execute(self, cls, statement, params, response=False):
        ...


class DynamoDBBackend(FlexBackend):
    import boto3

    TYPES = {"str": "S", "int": "N"}

    dynamodb = boto3.resource("dynamodb", endpoint_url=os.environ["DYNAMODB"])

    class ResultList:
        response = None

        def __init__(self, cls, response):
            self.response = response
            self.cls = cls

        def all(self):
            return [self.cls(**item) for item in self.response["Items"]]

        def first(self):
            return [self.cls(**item) for item in self.response["Items"]][0]

        def last(self):
            return [self.cls(**item) for item in self.response["Items"]][-1]

        def next(self):
            return "NEXT PAGE"

    def save(self, dataobject):
        _dao = asdict(dataobject)
        logging.info("Saving %s", _dao)
        table = self.dynamodb.Table(dataobject.__class__.__name__)

        from datetime import datetime

        curr_dt = datetime.now()

        timestamp = int(round(curr_dt.timestamp()))

        if hasattr(dataobject, "updated"):
            setattr(dataobject, "updated", timestamp)
        table.put_item(Item=_dao)

        return True

    def delete(self, cls_or_self, *args, **kwargs):
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

    def find(self, cls, match, response=False):
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

    def relation(self, dataobject, cls, backref=None, response=False):
        execute = getattr(cls, "execute")
        objects = execute(
            f'SELECT * FROM "{cls.__name__}" where {backref}=?',
            [dataobject.id],
            response=response,
        )
        return objects

    """
    ConsistentRead=True|False,
    NextToken='string',
    ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
    Limit=123"""
    def execute(self, cls, statement, params, response=False, consistentread=True, nexttoken=None, returnconsumedcapacity='NONE', limit=1):
        import botocore

        logging.debug("EXECUTE %s %s", statement, params)

        kwargs = {
            'ConsistentRead': consistentread,
            'ReturnConsumedCapacity': returnconsumedcapacity
            #'Limit': limit
        }
        if nexttoken:
            kwargs['NextToken'] = nexttoken

        try:
            output = self.dynamodb.meta.client.execute_statement(
                Statement=statement, Parameters=params, **kwargs
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
                return self.ResultList(cls, output)
            else:
                return [cls(**item) for item in output["Items"]]  # ResultList(output)

    @classmethod
    def create_table(self, cls, skip_exists=False):
        import botocore

        _class = cls
        _schema = {}

        for name, val in _class.__dict__.items():
            if name.find("_") == 0:
                continue
            if val.__class__.__name__ in self.TYPES:
                _schema[name] = val

        for base in _class.__bases__:
            for name, val in base.__dict__.items():
                if name.find("_") == 0:
                    continue
                if val.__class__.__name__ in self.TYPES:
                    _schema[name] = val

        schema = self.persist_data(cls)

        try:
            table = self.dynamodb.create_table(**schema)
            table.wait_until_exists()
        except botocore.exceptions.ClientError as ex:
            if not skip_exists:
                raise ex

        return schema

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
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        }

        return schema


class FlexBackendFactory:
    @classmethod
    def get(cls):
        return DynamoDBBackend()
