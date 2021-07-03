# Buying Robot on Binance
This is a simple personal robot for buying crypto currency on Binance

## Using docker

``` sh
# Build the image
docker build . -t binance-bot

# Run
docker run --rm --name binance-bot -v <path-to-config.yml>:/app/config.yml binance-bot python main.py config.yml <secret file> <from_asset> <target> <amount>

# e.g.:
docker run --rm --name binance-bot -v ~/binance-bot/config.yml:/app/config.yml binance-bot python main.py config.yml BUSD KSM 10
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
apiKey:
apiSecret: 
```