from common import read_secret
from trader import Trader
import sys


def main(args):
    if len(args) < 4:
        raise ValueError("Wrong args number")

    config = {
        "secret_file": args[0],
        "asset": args[1],
        "target": args[2],
        "amount": float(args[3])
    }

    secret = read_secret(config['secret_file'])
    trader = Trader(secret)
    trader.redeem_and_trade(
        config['aseet'],
        config['target'],
        config['amount'])


if __name__ == '__main__':
    main(sys.argv[1:])
