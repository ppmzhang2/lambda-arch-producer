from __future__ import annotations

import asyncio
import json
from typing import Awaitable, Callable, NoReturn

from app.finnhub_kafka import FinnHubProducer
from app.finnhub_ws import FinnHubWs

__all__ = ['Streamer']

from config import Config


class Streamer:
    __slots__ = ['_topic', '_finn_ws', '_finn_producer']

    def __init__(self):
        self._topic = Config.KAFKA_TOPIC
        self._finn_ws = FinnHubWs()
        self._finn_producer = FinnHubProducer()

    @staticmethod
    def _dict_to_bytes(dc: dict) -> bytes:
        # only ingest valid data
        if dc['type'] == 'trade':
            data = dc['data'][0]
            payload = f"{data['p']}, {data['s']}, {data['t']}, {data['v']}"
            b = json.dumps(payload).encode('utf8')
            return b
        raise ValueError('invalid input dict')

    async def _to_kafka(self, dc: dict) -> NoReturn:
        b = self._dict_to_bytes(dc)
        await self._finn_producer.send(self._topic, b)

    async def _to_console(self, dc: dict) -> NoReturn:
        b = self._dict_to_bytes(dc)
        print(b)

    def _stream(
        self,
        callback: Callable[[dict], Awaitable[NoReturn]],
        *symbols: str,
    ) -> NoReturn:
        return asyncio.run(self._finn_ws.trades_stream(
            callback,
            *symbols,
        ))

    def stream_to_kafka(self, *symbols: str) -> NoReturn:
        return self._stream(self._to_kafka, *symbols)

    def stream_to_console(self, *symbols: str) -> NoReturn:
        return self._stream(self._to_console, *symbols)
