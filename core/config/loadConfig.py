import json


def loadConfig():
    with open("configuration.json", "r") as cfg:
        return json.load(cfg)