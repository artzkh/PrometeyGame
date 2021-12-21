import http
from unittest import IsolatedAsyncioTestCase
from config import db


class TestDataBase(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await db.create()

    async def test_execute(self):

        # Test execute without fetch
        sql = "CREATE TABLE IF NOT EXISTS Test " \
              "(id BIGINT PRIMARY KEY, username VARCHAR(255))"
        result = await db.execute(sql, execute=True)
        expected = "CREATE TABLE"
        self.assertEqual(result, expected)

        sql = "INSERT INTO Test (id, username) " \
              "VALUES (1, 'test1'), (2, 'test2')"
        await db.execute(sql, execute=True)

        # Test execute with fetch
        sql = "SELECT * FROM Test"
        result = dict(await db.execute(sql, fetch=True))
        expected = {1: 'test1', 2: 'test2'}
        self.assertEqual(result, expected)

        # Test execute with fetch row
        sql = "SELECT * FROM Test"
        result = dict(await db.execute(sql, fetchrow=True))
        expected = {'id': 1, 'username': 'test1'}
        self.assertEqual(result, expected)

        # Test execute with fetch value
        sql = "SELECT * FROM Test"
        result = await db.execute(sql, fetchval=True)
        expected = 1
        self.assertEqual(result, expected)

        sql = "DROP TABLE Test"
        await db.execute(sql, execute=True)

    async def asyncTearDown(self):
        await db.close()
