import unittest
import redis
import json

from unittest.mock import MagicMock
from app.db import DBManager


class DBManagerTests(unittest.TestCase):
    def setUp(self):
        self.redis_mock = MagicMock(spec=redis.Redis)
        self.db_manager = DBManager(self.redis_mock)

    def test_write(self):
        name = 'test_name'
        data = {'key1': 'value1', 'key2': 'value2'}

        self.db_manager.write(name, data)

        data = json.dumps(data)
        self.redis_mock.set.assert_called_once_with(name, data)

    def test_read(self):
        name = 'test_name'
        expected_result = {'key1': 'value1', 'key2': 'value2'}

        self.redis_mock.get.return_value = json.dumps(
            expected_result, ensure_ascii=False
        ).encode('utf-8')
        result = self.db_manager.read(name)

        self.assertEqual(result, expected_result)
        self.redis_mock.get.assert_called_once_with(name)


if __name__ == '__main__':
    unittest.main()
