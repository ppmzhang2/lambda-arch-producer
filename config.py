import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # FinnHub API
    FINN_HUB_TOKEN = ''
    FINN_HUB_WS_PRE = 'wss://ws.finnhub.io'
    # Kafka
    KAFKA_BROKERS = 'localhost:9092'
    # path
    DB_DIR = ''.join([basedir, '/db'])
