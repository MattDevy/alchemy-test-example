import asyncio
import tornado.web
import json

from .models import KV
from .db import DB

from tornado.httpclient import HTTPResponse

from sqlalchemy import select
import sys

import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class PutHandler(tornado.web.RequestHandler):
    def initialize(self):
        print(type(DB()).__name__)
        self.session = DB().session

    def prepare(self):
        if self.request.headers["Content-Type"] == "application/json":
            self.args = json.loads(self.request.body)

    def put(self) -> HTTPResponse:
        key = self.args.get("key", None)
        value = self.args.get("value", None)
        if key is None or value is None:
            self.write({"error": "key or value is empty"})
        kv = KV(key=key, value=value)
        try:
            self.session.add(kv)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.write({"error": str(e)})


class GetHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = DB().session

    def get(self, key: str) -> HTTPResponse:
        try:
            kv = self.session.query(KV).filter(KV.key == key).first()
            self.write({"key": kv.key, "value": kv.value})
        except Exception as e:
            self.write({"error": str(e)})
            self.set_status(503)


def make_app():
    return tornado.web.Application([
        (r"/", PutHandler),
        (r"/(.*)", GetHandler)
    ])
