from fire import Fire

from app.streamer import Streamer


class Producer:
    _STREAMER = Streamer()

    def kafka(self, *symbols: str):
        return self._STREAMER.stream_to_kafka(*symbols)

    def console(self, *symbols: str):
        return self._STREAMER.stream_to_console(*symbols)


if __name__ == '__main__':
    Fire(Producer)
