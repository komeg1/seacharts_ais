from seacharts.core import Scope
from seacharts.core.ais import AISShipData

class AISParser:
    scope: Scope
    ships_info: list[AISShipData] = []

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
    
    def get_ships(self) -> list[list]:
        return self.read_ships()
    
    def read_ships(self) -> list[list]:
        ships = []
        with self.ships_list_lock:
            for row in self.ships_info:
                if row[1] == None or row[2] == None:
                    continue
                
                transformed_row = self.transform_ship(row)
                
                if transformed_row == (-1,-1,-1,-1,""):
                    continue
                if not self.scope.extent.is_in_bounding_box(transformed_row[1],transformed_row[2]):
                    continue
                ships.append(transformed_row)
        return ships
    
    def transform_ship(self, ship: AISShipData) -> tuple:
        try:
            mmsi = ship.mmsi
            if(self.scope.settings["enc"]["ais"]["coords_type"] != "utm"):
                lon, lat = self.convert_to_utm(ship.lon, ship.lat)
            else:
                lon = float(ship.lon)
                lat = float(ship.lat)
            heading = float(ship.heading) if ship.heading != '' else 0
            heading = heading if heading <= 360 else 0 
            color = ship.color
        except:
            return (-1,-1,-1,-1,"")
        return (mmsi, int(lon), int(lat), heading, color)
    
class AISShipData:
    mmsi: int
    lon: float
    lat: float
    turn: float
    speed: float
    course: float
    heading: int
    imo: int
    callsign: str
    shipname: str
    ship_type: int
    to_bow: int
    to_stern: int
    to_port: int
    to_starboard: int
    destination: str
    last_updated: float
    name: str
    ais_version: int
    ais_type: str
    status: str
    color: str

    def __init__(self, mmsi: int, lon: float, lat: float, turn: float, speed: float, course: float, heading: int, imo: int, callsign: str, shipname: str, ship_type: int, to_bow: int, to_stern: int, to_port: int, to_starboard: int, destination: str, last_updated: float, name: str, ais_version: int, ais_type: str, status: str):
        self.mmsi = mmsi
        self.lon = lon
        self.lat = lat
        self.turn = turn
        self.speed = speed
        self.course = course
        self.heading = heading
        self.imo = imo
        self.callsign = callsign
        self.shipname = shipname
        self.ship_type = ship_type
        self.to_bow = to_bow
        self.to_stern = to_stern
        self.to_port = to_port
        self.to_starboard = to_starboard
        self.destination = destination
        self.last_updated = last_updated
        self.name = name
        self.ais_version = ais_version
        self.ais_type = ais_type
        self.status = status
        self.color = "default"
    
