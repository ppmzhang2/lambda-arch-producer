from __future__ import annotations

import asyncio
import json
from typing import Callable, NoReturn, Awaitable

import websockets
from tenacity import retry, wait_fixed, retry_if_exception_type

from config import Config

__all__ = ['FinnHubWs']


class FinnHubWs(object):
    __slots__ = ['_uri']

    def __init__(self):
        self._uri = f'{Config.FINN_HUB_WS_PRE}?token={Config.FINN_HUB_TOKEN}'

    @retry(retry=retry_if_exception_type(ConnectionAbortedError),
           wait=wait_fixed(30))
    async def trades_stream(self, callback: Callable[[dict],
                                                     Awaitable[NoReturn]],
                            *symbols: str) -> NoReturn:
        """Stream real-time trades for US stocks, forex and crypto.

        :param callback: async callback function to consume each payload from
            stream
        :param symbols: symbols to subscribe
        :return:
        """
        async with websockets.connect(self._uri) as ws:
            send_tasks = (
                ws.send(f'{{"type":"subscribe","symbol":"{symbol}"}}')
                for symbol in symbols)
            await asyncio.gather(*send_tasks)
            while True:
                msg = await ws.recv()
                if msg is None:
                    raise ConnectionAbortedError('aborted')
                await callback(json.loads(msg))
