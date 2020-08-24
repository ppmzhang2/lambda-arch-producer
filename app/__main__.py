import sys
from typing import Optional

from app.trades_producer import TradesProducer

args = sys.argv[1:]

funcs = {
    'produce': (1, TradesProducer, TradesProducer.run)
}


def request() -> Optional[str]:
    """get the input request string, which will be then mapped as key to get
    main method

    :return:
    """
    try:
        return str(args[0])
    except IndexError:
        return None


def arg1() -> Optional[str]:
    try:
        return str(args[1]).split(',')
    except (IndexError, ValueError):
        return None


def main() -> None:
    if request() is None:
        raise TypeError('expect at least one input')

    n_args, cls, func = funcs.get(request(), (None, None, None))

    if func is None:
        raise TypeError('input request is not valid, accept only {}'.format(
            list(funcs.keys())))

    if n_args == 0:
        instance = cls()
        func(instance)
    elif n_args == 1 and (arg1() is None):
        raise TypeError('comma separated should be provided')
    elif n_args == 1:
        instance = cls()
        func(instance, *arg1())
    else:
        raise TypeError('input error')


if __name__ == '__main__':
    main()
