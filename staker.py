from common import read_secret
from binance.spot import Spot 


class Staker():
    def __init__(self, config):
        self.client = Spot(
            config['apiKey'],
            config['apiSecret'])

    def check_lending(self, asset="KSM"):
        params = {
            "asset": asset,
            "status": "ALL",
            "sortBy": "INTEREST_RATE"
        }
        return self.client.savings_project_list("ACTIVITY", **params)


if __name__ == '__main__':
    config = read_secret()
    staker = Staker(config)
    a = staker.check_lending()
    print(a)
