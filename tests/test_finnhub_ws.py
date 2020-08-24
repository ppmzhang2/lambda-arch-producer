import asyncio
import unittest

from app.finnhub_ws import FinnHubWs


class TestFinn(unittest.TestCase):
    loop = None
    SYMBOLS = ('FOREX:401484392', 'BINANCE:BTCUSDT')

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass started')
        cls.loop = asyncio.get_event_loop()
        print('setUpClass ended')

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass started')
        cls.loop.close()
        print('tearDownClass ended')

    def setUp(self):
        print('setUp started')
        self.loop = asyncio.get_event_loop()
        self.api = FinnHubWs()
        print('setUp ended')

    def tearDown(self):
        print('tearDown started')
        del self.api
        print('tearDown ended')

    def test_trades_stream(self):
        """checks FinnHubWs trades_stream methods

        methods:
          * FinnHubWs.trades_stream

        :return:
        """
        def checker(loop_, api_):
            async def helper(payload):
                print(payload)
                assert payload['type'] in {'trade', 'ping'}

            task = loop_.create_task(
                api_.trades_stream(helper, 'BINANCE:BTCUSDT'))

            try:
                loop_.call_later(10, task.cancel)
                loop_.run_until_complete(task)
            except asyncio.CancelledError:
                pass

        checker(self.loop, self.api)


if __name__ == '__main__':
    unittest.main(verbosity=2)
