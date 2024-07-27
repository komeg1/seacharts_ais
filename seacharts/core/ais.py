from seacharts.core import Scope

class AISParser:
    scope: Scope

    def __init__(self, scope: Scope):
        self.scope = scope

    def get_ships(self) -> list[tuple]:
        raise NotImplementedError