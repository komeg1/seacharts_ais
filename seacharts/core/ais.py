from seacharts.core import Scope
from pyproj import Proj
import csv
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
    
    def get_ships(self) -> list[tuple]:
        ship_list = self.read_ships()
        transformed_ships = [self.transform_ship(ship) for ship in ship_list]
        return transformed_ships
    
    def read_ships(self) -> list[list]:
        with open('data.csv', 'r', ) as f:
            reader = csv.reader(f)
            next(reader, None)
            ships = []
            ship_id = 0
            for row in reader:
                row[0] = ship_id
                ship_id += 1
                if row[1] == '' or row[2] == '':
                    continue
                ships.append(row)
        return ships
    
    def transform_ship(self, ship: list) -> tuple:
        mmsi = int(ship[0])
        if(self.scope.settings["enc"]["ais"]["coords_type"] != "utm"):
            lon, lat = self.convert_to_utm(float(ship[2]), float(ship[1]))
        lon = float(ship[2])
        lat = float(ship[1])
        heading = float(ship[3]) if ship[3] != '' else 0
        heading = heading if heading <= 360 else 0 
        color = ship[4]
        return (mmsi, int(lon), int(lat), heading, color)