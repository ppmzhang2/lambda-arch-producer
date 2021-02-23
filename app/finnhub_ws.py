from __future__ import annotations

import json
from asyncio import Semaphore, gather
from typing import Awaitable, Callable, NoReturn

import websockets
from tenacity import retry, retry_if_exception_type, wait_fixed
from websockets.client import WebSocketClientProtocol

from config import Config

__all__ = ['FinnHubWs']


class FinnHubWs:
    __slots__ = ['_sem', '_uri']

    def __init__(self, limit: int = 5):
        self._sem = Semaphore(limit)
        self._uri = f'{Config.FINN_HUB_WS_PRE}?token={Config.FINN_HUB_TOKEN}'

    async def _semaphored_send(self, wscp: WebSocketClientProtocol, msg: str):
        async with self._sem:
            return await wscp.send(msg)

    @retry(retry=retry_if_exception_type(ConnectionAbortedError),
           wait=wait_fixed(30))
    async def trades_stream(
        self,
        callback: Callable[[dict], Awaitable[NoReturn]],
        *symbols: str,
    ) -> NoReturn:
        """Stream real-time trades for US stocks, forex and crypto.

        :param callback: async callback function to consume each payload from
            stream
        :param symbols: symbols to subscribe
        :return:
        """
        messages = [
            f'{{"type":"subscribe","symbol":"{symbol}"}}' for symbol in symbols
        ]

        async with websockets.connect(self._uri) as ws:
            send_tasks = (self._semaphored_send(ws, msg) for msg in messages)
            await gather(*send_tasks)
            while True:
                msg = await ws.recv()
                if msg is None:
                    raise ConnectionAbortedError('aborted')
                await callback(json.loads(msg))
