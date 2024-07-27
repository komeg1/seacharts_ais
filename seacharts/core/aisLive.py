from seacharts.core import AISParser, Scope
from pyais import decode
from pyais.stream import TCPConnection
from pyais import AISTracker
#from seacharts.display.colors import _ship_colors
from random import random
import csv

class AISLiveParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self.host = self.scope.settings["enc"]["ais"]["address"]
        self.port = self.scope.settings["enc"]["ais"]["port"]

    def get_ships(self) -> list[tuple]:
        self.listen_stream()
        ships = self.read_ships()
        transformed_ships = [self.transform_ship(ship) for ship in ships]
        return transformed_ships

    def listen_stream(self)->None:
        print("Listening to stream {host}:{port}", self.host, self.port)
        with AISTracker() as tracker:
            self.get_current_data(tracker)
            for msg in TCPConnection(self.host,port=self.port):
                decoded_message = msg.decode()
                ais_content = decoded_message
                tracker.update(msg)
    
    def get_current_data(self, tracker: AISTracker)->None:
        print("saving data to csv")
        with open('data.csv', 'w') as f:
            fieldnames = ['mmsi', 'long', 'lat', 'heading', 'color']
            writer = csv.writer(f, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ship in tracker.tracks:
                writer.writerow({'mmsi': ship.mmsi, 'long': ship.lon, 'lat': ship.lat, 'heading': ship.heading, 'color': ""})

    def read_ships(self) -> list:
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            ships = []
            for row in reader:
                ships.append(row)
        return ships

    def transform_ship(self, ship: list) -> tuple:
        mmsi = ship[0]
        lon, lat = self.convert_to_utm(ship[1], ship[2])
        heading = ship[3] if ship[3] <= 360 else 0 
        #color = random.choice(list(_ship_colors.keys()))
        color = "red"
        return (mmsi, lon, lat, heading, color)
    
    def convert_to_utm(self, lon: float, lat: float) -> tuple:
        return (lon, lat)
