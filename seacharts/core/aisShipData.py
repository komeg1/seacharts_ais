
class AISShipData:
    mmsi: str
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

    def __init__(self, color: str = None, mmsi: str = None, lon: float = None, lat: float = None, turn: float = None, 
                 speed: float = None, course: float = None, heading: int = None, imo: int = None, callsign: str = None, 
                 shipname: str = None, ship_type: int = None, to_bow: int = None, to_stern: int = None, to_port: int = None, 
                 to_starboard: int = None, destination: str = None, last_updated: float = None, name: str = None, 
                 ais_version: int = None, ais_type: str = None, status: str = None):
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
        from seacharts.core.ais import AISParser
        self.color = AISParser.color_resolver(ship_type)

    