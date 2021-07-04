from common import read_secret
from binance.spot import Spot 
import json
import time
import requests


class Trader():
    def __init__(self, config, base_url=None):
        if base_url:
            self.client = Spot(
                config['apiKey'],
                config['apiSecret'],
                base_url=base_url)
        else:
            self.client = Spot(
                config['apiKey'],
                config['apiSecret'])
        if 'uid' in config and 'webhook' in config:
            self.call_webhook = True
            self.uid = config['uid']
            self.webhook = config['webhook']

    def get_all_flexible_product_positions(self, asset="BUSD"):
        flexible_positions = \
            self.client.savings_flexible_product_position(asset=asset)
        flexible_positions = \
            sorted(
                flexible_positions,
                key=lambda x: x['avgAnnualInterestRate']
            )
        return flexible_positions

    def check_flexible_product(self, asset="BUSD", amount=10):
        flexible_positions = \
            self.get_all_flexible_product_positions(asset=asset)
        for position in flexible_positions:
            if float(position['totalAmount']) >= amount:
                return position['productId']
        return None

    def redeem_balance(self, asset="BUSD", amount=10):
        productId = \
           self.check_flexible_product(asset=asset, amount=amount)
        if not productId:
            raise ValueError("Balance not enough")
        return self.client.savings_flexible_redeem(productId, amount, "FAST")

    def make_trade(self, symbol="KSMBUSD", amount=10, is_test=False):
        params = {
            'symbol': symbol,
            'side': 'BUY',
            'type': 'MARKET',
            'quoteOrderQty': amount,
        }
        if is_test:
            response = self.client.new_order_test(**params)
        else:
            response = self.client.new_order(**params)
        return response

    def redeem_and_trade(self, asset, target, amount):
        amount = self.round_quantity(amount)
        self.redeem_balance(asset, amount)
        # not sure redeem is async or not
        time.sleep(1)
        res = self.make_trade(symbol=f"{target}{asset}", amount=amount)
        if self.call_webhook:
            payload = self.generate_webhook_content(
                res,
                "buy",
            )
            self.post_webhook(payload)

    def post_webhook(self, payload):
        data = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}
        requests.request("POST", self.webhook, headers=headers, data=data)

    def generate_webhook_content(self, response, action, precision=6):
        fills = response['fills']
        cost, qty = 0, 0
        for fill in fills:
            cost += float(fill['price']) * float(fill['qty']) \
                + float(fill['commission'])
            qty += float(fill['qty'])

        return {
            "uid": self.uid,
            "symbol": response['symbol'],
            "action": action,
            "average_cost": round(cost / qty, precision),
            "qty": round(qty, precision)
        }

    def operate_webhook_content(self, symbol, action, average_cost, qty):
        return {
            "uid": self.uid,
            "symbol": symbol,
            "action": action,
            "average_cost": average_cost,
            "qty": qty
        }

    @classmethod
    def round_quantity(cls, quantity, precision=6):
        return float(round(quantity, precision))


def test_get_flexible_positions():
    config = read_secret()
    # base_url='https://testnet.binance.vision'
    base_url = None
    trader = Trader(config=config, base_url=base_url)

    # asset = "BNB"
    asset = "BUSD"
    positions = trader.get_all_flexible_product_positions(asset=asset)
    print(positions)


def test_redeem():
    config = read_secret()
    # base_url='https://testnet.binance.vision'
    base_url = None
    trader = Trader(config=config, base_url=base_url)

    # asset = "BNB"
    asset = "BUSD"
    positions = trader.get_all_flexible_product_positions(asset=asset)
    print(positions)

    amount = 10
    res = trader.redeem_balance(asset=asset, amount=amount)
    print(res)

    positions = trader.get_all_flexible_product_positions(asset=asset)
    print(positions)


def test_trade():
    config = read_secret()
    # base_url='https://testnet.binance.vision'
    base_url = None
    trader = Trader(config=config, base_url=base_url)

    symbol = "KSMBUSD"
    amount = 10
    is_test = False
    amount = trader.round_quantity(amount)
    res = trader.make_trade(symbol=symbol, amount=amount, is_test=is_test)
    print(res)
    print(trader.process_trade_response(res))


def test_integration(symbol):
    config = read_secret()
    trader = Trader(config=config)
    payload = trader.operate_webhook_content("SOLBUSD", "buy", 34.392, 0.29)
    trader.post_webhook(payload)


if __name__ == '__main__':
    # test_get_flexible_positions()
    # test_trade()
    test_integration("SOLBUSD")
