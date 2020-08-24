from __future__ import annotations

from typing import Callable, NoReturn, Awaitable

from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer, ConsumerRecord

from config import Config

__all__ = ['FinnHubProducer', 'FinnHubConsumer']


class FinnHubProducer(object):
    __slots__ = ['_brokers']

    def __init__(self):
        self._brokers = Config.KAFKA_BROKERS

    async def send(self, topic: str, msg: bytes):
        _producer = AIOKafkaProducer(bootstrap_servers=self._brokers)
        await _producer.start()
        try:
            await _producer.send_and_wait(topic, msg)
        finally:
            await _producer.stop()


class FinnHubConsumer(object):
    __slots__ = ['_brokers', '_offset', '_topic']

    def __init__(self, offset: str, topic: str):
        self._brokers = Config.KAFKA_BROKERS
        self._offset = offset
        self._topic = topic

    async def recv(self, callback: Callable[[ConsumerRecord],
                                            Awaitable[NoReturn]]):
        _consumer = AIOKafkaConsumer(
            self._topic,
            auto_offset_reset=self._offset,
            bootstrap_servers=self._brokers,
        )
        await _consumer.start()
        try:
            async for msg in _consumer:
                await callback(msg)
        finally:
            await _consumer.stop()
