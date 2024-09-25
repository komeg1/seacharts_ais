from seacharts.core import AISParser, Scope
from pyais.stream import TCPConnection
from pyais import AISTracker
import threading

class AISLiveParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self.host = self.scope.settings["enc"]["ais"]["address"]
        self.port = self.scope.settings["enc"]["ais"]["port"]
        self.interval = self.scope.settings["enc"]["ais"]["interval"]
        self.clear_threshold = {
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 2592000,
            "year": 31536000
        }
        self.ttl_value = self.clear_threshold[self.scope.time.period]*self.scope.time.period_mult
        self.ships_info = []
        self.ais = AISTracker(ttl_in_seconds=self.ttl_value)
        threading.Thread(target=self.start_stream_listen).start()

    def get_ships(self) -> list[tuple]:
        ship_list = self.read_ships()
        return ship_list

    def start_stream_listen(self)->None:
        print("Listening to stream {host}:{port}", self.host, self.port)
        with self.ais as tracker:
            t = threading.Timer(self.interval, self.get_current_data, [tracker])
            t.start()
            for msg in TCPConnection(self.host,port=self.port):
                tracker.update(msg)
    
    def get_current_data(self, tracker: AISTracker) -> None:    
        for ship in tracker.tracks:
            self.ships_info.append([ship.mmsi,ship.lon, ship.lat, ship.heading, "", ship.last_updated])
        timer = threading.Timer(self.interval, self.get_current_data, [tracker])
        timer.start()

    def read_ships(self) -> list[list]:
        ships = []
        for row in self.ships_info:
            if row[1] == None or row[2] == None:
                continue
            transformed_row = self.transform_ship(row)
            ships.append(transformed_row)
        return ships

    def transform_ship(self, ship: list) -> tuple:
        mmsi = int(ship[0])
        try:
            lon, lat = self.convert_to_utm(float(ship[2]), float(ship[1]))
        except:
            lon, lat = 0, 0
        heading = float(ship[3]) if ship[3] != None else 0
        heading = heading if heading <= 360 else 0 
        color = "red"
        return (mmsi, lon, lat, heading, color)
