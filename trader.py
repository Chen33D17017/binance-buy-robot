from common import read_secret
from binance.spot import Spot 
import time


class Trader():
    def __init__(self, config):
        self.client = Spot(
            config['apiKey'],
            config['apiSecret'])

    def check_flexible_product(self, asset="BUSD", amount=10):
        flexible_positions = \
            self.client.savings_flexible_product_position(asset="BUSD")
        for position in flexible_positions:
            if float(position['totalAmount']) >= amount:
                return position['productId']
        return None

    def redeem_balance(self, asset="BUSD", amount=10):
        productId = \
           self.client.check_flexible_product(asset=asset, amount=amount)
        if not productId:
            raise ValueError("Balance not enough")
        self.client.savings_flexible_redeem(productId, amount, "FAST")

    def make_trade(self, symbol="KSMBUSD", amount=10):
        params = {
            'symbol': symbol,
            'side': 'BUY',
            'type': 'MARKET',
            'quoteOrderQty': amount,
        }
        response = self.client.new_order(**params)
        return response

    def redeem_and_trade(self, asset, target, amount):
        self.redeem_balance(asset, amount)
        # not sure redeem is async or not
        time.sleep(1)
        self.make_trade(symbol=f"{target}{asset}", amount=amount)


if __name__ == '__main__':
    secret = read_secret()
    trader = Trader(secret)
    trader.make_trade()
