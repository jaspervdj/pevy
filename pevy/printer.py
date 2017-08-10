class Printer:
    def __init__(self, logger):
        self.logger = logger

    def print(self, item):
        print('>>> ' + item.text)
