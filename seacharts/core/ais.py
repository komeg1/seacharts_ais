from seacharts.core import Scope
from pyproj import Proj

class AISParser:
    scope: Scope

    def __init__(self, scope: Scope):
        self.scope = scope

    def get_ships(self) -> list[tuple]:
        raise NotImplementedError
    
    def convert_to_utm(self, x: int, y: int) -> tuple[int, int]:
        p = Proj(proj='utm', zone=33, ellps='WGS84')
        return p(x, y)
    