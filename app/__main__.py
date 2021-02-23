from fire import Fire

from app.trades_producer import TradesProducer


class Producer:
    _PRODUCER = TradesProducer()

    def kafka(self, *symbols: str):
        return self._PRODUCER.run(*symbols)


if __name__ == '__main__':
    Fire(Producer)
