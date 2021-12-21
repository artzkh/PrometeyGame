import time
from unittest import IsolatedAsyncioTestCase

from config import db
from functions import calculate_indicators


class TestIndicators(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await db.create()
        await db.add_user(1, "test")

    async def test_changes(self):

        # health=100 happiness=100 satiety=100 hygiene=100 energy=100
        await calculate_indicators(1, time.time())
        result = list(await db.get_user_indicators(1))
        self.assertEqual(result, [100, 100, 100, 100, 100])

        # health=100 happiness=30 satiety=30 hygiene=30 energy=30
        await calculate_indicators(1, time.time()-21000)
        result = list(await db.get_user_indicators(1))
        self.assertEqual(result, [100, 30, 30, 30, 30])

        # health=100 happiness=0 satiety=0 hygiene=0 energy=0
        await calculate_indicators(1, time.time()-9000)
        result = list(await db.get_user_indicators(1))
        self.assertEqual(result, [100, 0, 0, 0, 0])

        # health=99.9 happiness=0 satiety=0 hygiene=0 energy=0
        await calculate_indicators(1, time.time()-1)
        result = list(await db.get_user_indicators(1))
        assert result[0] < 100

    async def test_recommendations(self):

        # result = []
        result = await calculate_indicators(1, time.time())
        self.assertEqual(len(result), 0)

        # result = ['happiness', 'satiety', 'hygiene', 'energy']
        result = await calculate_indicators(1, time.time()-21000)
        self.assertEqual(len(result), 4)

        # result = ['health', 'happiness', 'satiety', 'hygiene', 'energy']
        result = await calculate_indicators(1, time.time()-9500)
        self.assertEqual(len(result), 5)

        # result=False
        result = await calculate_indicators(1, time.time()-43000)
        self.assertFalse(result)

    async def asyncTearDown(self):
        await db.del_user(1)
        await db.close()
