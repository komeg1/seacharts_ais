from seacharts.core import AISParser, Scope
from pyais import decode
from pyais.stream import TCPConnection
from pyais import AISTracker
#from seacharts.display.colors import _ship_colors
from random import random
import csv
import threading

class AISLiveParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self.host = self.scope.settings["enc"]["ais"]["address"]
        self.port = self.scope.settings["enc"]["ais"]["port"]
        threading.Thread(target=self.start_stream_listen).start()

    def get_ships(self) -> list[tuple]:
        ship_list = self.read_ships()
        print(ship_list)
        transformed_ships = [self.transform_ship(ship) for ship in ship_list]
        return transformed_ships

    def start_stream_listen(self)->None:
        print("Listening to stream {host}:{port}", self.host, self.port)
        with AISTracker() as tracker:
            t = threading.Timer(30, self.get_current_data, [tracker])
            t.start()
            for msg in TCPConnection(self.host,port=self.port):
                tracker.update(msg)
    
    def get_current_data(self, tracker: AISTracker) -> None:    
        print(f'Snapshot taken and saved at {tracker.last_updated}')
        with open('data.csv', 'w', newline='') as f:
            fieldnames = ['mmsi', 'long', 'lat', 'heading', 'color']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ship in tracker.tracks:
                writer.writerow({'mmsi': ship.mmsi, 'long': ship.lon, 'lat': ship.lat, 'heading': ship.heading, 'color': ""})
        timer = threading.Timer(30, self.get_current_data, [tracker])
        timer.start()

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
        color = "red"
        return (mmsi, lon, lat, heading, color)
