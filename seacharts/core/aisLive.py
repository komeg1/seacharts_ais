from seacharts.core import AISParser

class AISLiveParser(AISParser):
    def __init__(self):
        self.host = self.scope.settings["enc"]["ais"]["host"]
        self.port = self.scope.settings["enc"]["ais"]["port"]

    def get_ships(self) -> list:
        pass