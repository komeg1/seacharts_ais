from seacharts.core import Scope
from pyproj import Proj
import csv
class AISParser:
    scope: Scope

    def __init__(self, scope: Scope):
        self.scope = scope
        self.ships_info = []

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
    
    def get_ships(self) -> list[list]:
        return self.read_ships()
    
    def read_ships(self) -> list[list]:
        ships = []
        with self.ships_list_lock:
            print(len(self.ships_info))
            for row in self.ships_info:
                if row[1] == None or row[2] == None:
                    continue
                transformed_row = self.transform_ship(row)
                ships.append(transformed_row)
        return ships
    
    def transform_ship(self, ship: list) -> tuple:
        try:
            mmsi = int(ship[0])
            if(self.scope.settings["enc"]["ais"]["coords_type"] != "utm"):
                lon, lat = self.convert_to_utm(float(ship[2]), float(ship[1]))
            else:
                lon = float(ship[2])
                lat = float(ship[1])
            heading = float(ship[3]) if ship[3] != '' else 0
            heading = heading if heading <= 360 else 0 
            color = ship[4]
        except:
            return
        return (mmsi, int(lon), int(lat), heading, color)