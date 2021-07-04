# Buying Robot on Binance
This is a simple personal robot for buying crypto currency on Binance

## Using docker

``` sh
# Build the image
docker build . -t binance-bot

# Run
docker run --rm --name binance-bot -v <path-to-config.yml>:/app/config.yml binance-bot python main.py config.yml <secret file> <from_asset> <target> <amount>

# e.g.:
docker run --rm --name binance-bot -v ~/projects/binance-buy-robot/config.yml:/app/config.yml binance-bot python main.py config.yml BUSD KSM 10
```

## Run script periodically (using crontab)

``` sh
crontab -e
# Then add the following line into the file, this example runs at 8:00am everyday
0 8 * * * docker run --rm --name binance-bot -v ~/binance-buy-robot/config.yml:/app/config.yml binance-bot python main.py config.yml BUSD KSM 10 >> ~/projects/binance-buy-robot/log.txt
```

## Dependency
Install following dependency(python3):

``` sh
pip install pyyaml
pip install binance-connector

# Or simply
pip install -r requirements.txt
```
## How to use
simplely execute following command

``` sh
python main.py <secret file> <from_asset> <target> <amount>

# e.g.: buy 10 BUSD-worth KSM coins
python main.py config.yml BUSD KSM 10
```

secret file need to be yaml file and contain:

```yaml
uid:
webhook:
apiKey:
apiSecret: 
```

## Calling Webhook
If you assign webhook & uid in your config file, robot will call your webhook with POST request
payload example:

```json
{
    "uid": "uid",
    "symbol": "KSMBUSD",
    "action": "buy",
    "average_cost": 15.872,
    "qty": 1
}
```