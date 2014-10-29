import configparser


class Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('bonsho.ini')

    def __getitem__(self, k):
        return self.config[k]
