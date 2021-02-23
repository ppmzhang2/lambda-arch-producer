from __future__ import annotations

import asyncio
import json
from typing import NoReturn

from app.finnhub_kafka import FinnHubProducer
from app.finnhub_ws import FinnHubWs

__all__ = ['TradesProducer']

from config import Config


class TradesProducer:
    __slots__ = ['_topic', '_finn_ws', '_finn_producer']

    def __init__(self):
        self._topic = Config.KAFKA_TOPIC
        self._finn_ws = FinnHubWs()
        self._finn_producer = FinnHubProducer()

    async def send_trades(self, *symbols: str):
        async def cb(dc: dict):
            # only ingest valid data
            if dc['type'] == 'trade':
                data = dc['data'][0]
                payload = f"{data['p']}, {data['s']}, {data['t']}, {data['v']}"
                b = json.dumps(payload).encode('utf8')
                await self._finn_producer.send(self._topic, b)

        await self._finn_ws.trades_stream(cb, *symbols)

    def run(self, *symbols: str) -> NoReturn:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_trades(*symbols))
