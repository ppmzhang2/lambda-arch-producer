# Lambda Architecture - Kafka Producer

Produce real-time trades for US stocks, forex and crypto to Kafka from [Finnhub](https://finnhub.io/).

## Usage

1. Push finnhub trade stream to the Kafaka by adding symbols of Us stocks, forex and crypto, separated by comma:

    ```sh
    python -m app produce BINANCE:BTCUSDT,AMZN
    ```

## Reference

1. https://finnhub.io/docs/api
