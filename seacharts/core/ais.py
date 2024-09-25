from seacharts.core import Scope

class AISParser:
    scope: Scope

    def __init__(self, scope: Scope):
        self.scope = scope

    def get_ships(self) -> list[tuple]:
        raise NotImplementedError
    
    def convert_to_utm(self, x: float, y: float) -> tuple[int, int]:
        if not self.validate_lon_lat(x, y):
            return (0, 0)
        return self.scope.extent.convert_lat_lon_to_utm(x, y)
    
    def validate_lon_lat(self, lon: float, lat: float) -> bool:
        if -180 <= lon <= 180 and -90 <= lat <= 90:
            return True
        return False
    