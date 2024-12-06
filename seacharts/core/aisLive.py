from seacharts.core import AISParser, Scope
from seacharts.core.aisShipData import AISShipData
from pyais.stream import TCPConnection
from pyais import AISTracker, AISTrack
import threading
from datetime import datetime

class AISLiveParser(AISParser):
    """
    Class for parsing AIS data from live stream

    """
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
        self.ships_info = []
        self.ships_list_lock = threading.Lock()
        self.ttl_value = self.clear_threshold[self.scope.time.period]*self.scope.time.period_mult
        self.ais = AISTracker(ttl_in_seconds=self.ttl_value)
        threading.Thread(target=self.start_stream_listen, daemon=True).start()


        if self.scope.settings["enc"]["ais"].get("dynamic_scale") == True:
            self._dynamic_scale = True
        else:
            self._dynamic_scale = False
        self._user_scale = 1.0 if self.scope.settings["enc"]["ais"].get("scale") is None else self.scope.settings["enc"]["ais"]["scale"]

    def get_ships(self) -> list[tuple]:
        """
        Retrieve list of ships received from AIS stream

        :return: list of ships with format (mmsi, lon, lat, heading, color)
        :rtype: list[tuple]
        """
        ship_list = self.read_ships()
        return ship_list

    def start_stream_listen(self)->None:
        """
        Start listening to AIS stream using AIS Tracker based on connection setting from config.yaml

        :return: None
        """
        print("Listening to stream {host}:{port}", self.host, self.port)
        with self.ais as tracker:
            t = threading.Timer(self.interval, self.get_current_data, [tracker])
            t.start()
            for msg in TCPConnection(self.host,port=self.port):
                tracker.update(msg)
    
    def get_current_data(self, tracker: AISTracker) -> None:
        """
        Append newest data to ships_info list and start timer for next data retrieval

        :param tracker: AISTracker object
        :return: None
        """
        with self.ships_list_lock:
            self.ships_info.clear()
            for ship in tracker.tracks:
                aisship = AISLiveShipData(ship)
                self.ships_info.append(aisship)
        timer = threading.Timer(self.interval, self.get_current_data, [tracker])
        timer.start()

    def transform_ship(self, ship: AISShipData) -> tuple:
        """
        Transform ship data to format (mmsi, lon, lat, heading, color)

        :param ship: list of ship data gathered by AIS Tracker
        :type ship: list
        :return: ship data with format (mmsi, lon, lat, heading, color)
        :rtype: tuple
        """
        try:
            mmsi = ship.mmsi
            lat, lon = self.convert_to_utm(float(ship.lat), float(ship.lon))
            heading = float(ship.heading) if ship.heading != None else 0
            heading = heading if heading <= 360 else 0 
            color = ship.color
            if(ship.to_bow is not None):
                scale = self.calculate_scale({"to_bow": ship.to_bow,"to_stern":ship.to_stern,"to_port":ship.to_port,"to_starboard":ship.to_starboard})
                return (mmsi, int(lat), int(lon), heading, color,scale)
        except:
            return (-1,-1,-1,-1,"")
        return (mmsi, int(lat), int(lon), heading, color, self._user_scale)

    

class AISLiveShipData(AISShipData):
    def __init__(self, aistrack: AISTrack):
        self.mmsi = aistrack.mmsi
        self.lon = aistrack.lon
        self.lat = aistrack.lat
        self.turn = aistrack.heading
        self.ship_type = aistrack.ship_type
        self.last_updated = datetime.fromtimestamp(aistrack.last_updated).strftime('%d-%m-%Y %H:%M:%S')
        self.name = aistrack.name
        self.ais_version = aistrack.ais_version
        self.ais_type = aistrack.ais_type
        self.status = aistrack.status
        self.course = aistrack.course
        self.speed = aistrack.speed
        self.heading = aistrack.heading
        self.imo = aistrack.imo
        self.callsign = aistrack.callsign
        self.shipname = aistrack.shipname
        self.to_bow = aistrack.to_bow
        self.to_stern = aistrack.to_stern
        self.to_port = aistrack.to_port
        self.to_starboard = aistrack.to_starboard
        self.destination = aistrack.destination
        self.ship_type = aistrack.ship_type
        self.color = AISParser.color_resolver(aistrack.ship_type)