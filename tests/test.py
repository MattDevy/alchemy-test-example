from unittest import mock, main
from tornado.testing import AsyncHTTPTestCase
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from src.web import make_app
from src.db import DB
from src.models import KV
import json


class FakeDB:
    def __init__(self, session):
        self.session = session


class GetKVTestCase(AsyncHTTPTestCase):
    def get_app(self):
        session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(KV),
                        mock.call.filter(KV.key == "name")],
                    [KV(key="name", value="Matt")]
                )
            ]
        )
        self.session = session
        DB._instance = FakeDB(session)
        return make_app()

    def test_get(self):
        response = self.fetch("/name")
        # asset mock was called once
        self.assertEqual(self.session.query.call_count, 1)
        self.assertEqual(self.session.filter.call_count, 1)

        # assert 200 OK and correct body
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), {"key": "name", "value": "Matt"})
        


if __name__ == "__main__":
    main()
