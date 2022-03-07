from json import load

def check_write():
    with open('config.json', "r") as config:
        config = load(config)
        if config["write"] == "y":
            return True
        else:
            return False
