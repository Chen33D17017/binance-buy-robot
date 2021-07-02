import yaml


def read_secret(filename='config.yml'):
    with open(filename, "r") as rf:
        secret = yaml.safe_load(rf)
    return secret
