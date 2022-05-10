import json

class ConfigReader:
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as f:
            self.data = json.load(f)
