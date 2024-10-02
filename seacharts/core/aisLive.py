from seacharts.core import AISParser, Scope
from pyais import decode
from pyais.stream import TCPConnection
from pyais import AISTracker
#from seacharts.display.colors import _ship_colors
from random import random
import csv
import threading
import time
from datetime import datetime
class AISLiveParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self.host = self.scope.settings["enc"]["ais"]["address"]
        self.port = self.scope.settings["enc"]["ais"]["port"]
        self.interval = self.scope.settings["enc"]["ais"]["interval"]
        self.cnt = 1210
        threading.Thread(target=self.start_stream_listen).start()

    def get_ships(self) -> list[tuple]:
        ship_list = self.read_ships()
        transformed_ships = [self.transform_ship(ship) for ship in ship_list]
        return transformed_ships

    def start_stream_listen(self)->None:
        print("Listening to stream {host}:{port}", self.host, self.port)
        with AISTracker() as tracker:
            t = threading.Timer(self.interval, self.get_current_data, [tracker])
            t.start()
            for msg in TCPConnection(self.host,port=self.port):
                tracker.update(msg)
    
    def get_current_data(self, tracker: AISTracker) -> None:    
        print(f'Snapshot taken and saved at {time.ctime()}')
        with open('data.csv', 'a+', newline='') as f:
            fieldnames = ['ID','latitude','longtitude','heading','color','timestamp','mmsi']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ship in tracker.tracks:
                self.cnt+=1
                writer.writerow({'ID': self.cnt,'latitude':ship.lat,'longtitude':ship.lon,'heading':ship.heading,'color':"red","timestamp":datetime.fromtimestamp(ship.last_updated).strftime("%d-%m-%Y %H:%M:%S"),"mmsi":ship.mmsi})
                
        timer = threading.Timer(self.interval, self.get_current_data, [tracker])
        timer.start()

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
        lon, lat = self.convert_to_utm(float(ship[2]), float(ship[1]))
        heading = float(ship[3]) if ship[3] != '' else 0
        heading = heading if heading <= 360 else 0 
        color = "red"
        return (mmsi, lon, lat, heading, color)

    def color_resolver(self,msg):
        if msg is None:
            return "default"
        if isinstance(msg,str):
            return msg
        
        msg = int(msg)
        if msg == 0:
            return  'default' 
        elif 1 <= msg <= 19:
            return  'default'   # Reserved for future use
        elif msg == 20:
            return  'WIG' 
        elif msg == 21:
            return  'WIG_A' 
        elif msg == 22:
            return  'WIG_B' 
        elif msg == 23:
            return  'WIG_C' 
        elif msg == 24:
            return  'WIG_D' 
        elif 25 <= msg <= 29:
            return  'WIG'   # Reserved for future use
        elif msg == 30:
            return  'FISHING' 
        elif msg == 31:
            return  'TOWING' 
        elif msg == 32:
            return  'TOWING_EXCEED' 
        elif msg == 33:
            return  'DREDGING_UNDERWATER' 
        elif msg == 34:
            return  'DIVING_OPS' 
        elif msg == 35:
            return  'MILITARY_OPS' 
        elif msg == 36:
            return  'SAILING' 
        elif msg == 37:
            return  'PLEASURE_CRAFT' 
        elif 38 <= msg <= 39:
            return  'default'  
        elif msg == 40:
            return  'HSC' 
        elif msg == 41:
            return  'HSC_A' 
        elif msg == 42:
            return  'HSC_B' 
        elif msg == 43:
            return  'HSC_C' 
        elif msg == 44:
            return  'HSC_D' 
        elif 45 <= msg <= 49:
            return  'HSC'   
        elif msg == 50:
            return  'PILOT' 
        elif msg == 51:
            return  'RESCUE' 
        elif msg == 52:
            return  'TUG' 
        elif msg == 53:
            return  'PORT_TENDER' 
        elif msg == 54:
            return  'ANTI_POLLUTION_EQ' 
        elif msg == 55:
            return  'LAW_ENFORCEMENT' 
        elif 56 <= msg <= 57:
            return  'LOCAL_VESSEL'   
        elif msg == 58:
            return  'MEDICAL_TRANSPORT' 
        elif msg == 59:
            return  'NONCOMBATANT' 
        elif msg == 60:
            return  'PASSENGER' 
        elif msg == 61:
            return  'PASSENGER_A' 
        elif msg == 62:
            return  'PASSENGER_B' 
        elif msg == 63:
            return  'PASSENGER_C' 
        elif msg == 64:
            return  'PASSENGER_D' 
        elif 65 <= msg <= 68:
            return  'PASSENGER'   
        elif msg == 69:
            return  'PASSENGER'  
        elif msg == 70:
            return  'CARGO' 
        elif msg == 71:
            return  'CARGO_A' 
        elif msg == 72:
            return  'CARGO_B' 
        elif msg == 73:
            return  'CARGO_C' 
        elif msg == 74:
            return  'CARGO_D' 
        elif 75 <= msg <= 78:
            return  'CARGO'   # Reserved for future use
        elif msg == 79:
            return  'CARGO'   # No additional info
        elif msg == 80:
            return  'TANKER' 
        elif msg == 81:
            return  'TANKER_A' 
        elif msg == 82:
            return  'TANKER_B' 
        elif msg == 83:
            return  'TANKER_C' 
        elif msg == 84:
            return  'TANKER_D' 
        elif 85 <= msg <= 88:
            return  'TANKER'   # Reserved for future use
        elif msg == 89:
            return  'TANKER'   # No additional info
        elif msg == 90:
            return  'OTHER' 
        elif msg == 91:
            return  'OTHER_A' 
        elif msg == 92:
            return  'OTHER_B' 
        elif msg == 93:
            return  'OTHER_C' 
        elif msg == 94:
            return  'OTHER_D' 
        elif 95 <= msg <= 98:
            return  'OTHER'   # Reserved for future use
        elif msg == 99:
            return  'OTHER'   # No additional info
        else:
            return  'default' 