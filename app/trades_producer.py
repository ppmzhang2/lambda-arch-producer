from __future__ import annotations

import asyncio
import json
from typing import NoReturn

from app.finnhub_kafka import FinnHubProducer
from app.finnhub_ws import FinnHubWs

__all__ = ['TradesProducer']

from config import Config


class TradesProducer(object):
    __slots__ = ['_topic', '_symbols', '_finn_ws', '_finn_producer']

    def __init__(self, *symbols: str):
        self._topic = Config.KAFKA_TOPIC
        self._symbols = symbols
        self._finn_ws = FinnHubWs()
        self._finn_producer = FinnHubProducer()

    async def send_trades(self):
        async def cb(dc: dict):
            print(dc)
            b = json.dumps(dc).encode('utf8')
            await self._finn_producer.send(self._topic, b)

        await self._finn_ws.trades_stream(cb, *self._symbols)

    def run(self) -> NoReturn:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_trades())
