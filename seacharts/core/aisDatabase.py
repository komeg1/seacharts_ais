from seacharts.core import AISParser, Scope
#from seacharts.display.colors import _ship_colors
from random import random
import csv
import threading
import time
from datetime import datetime
import sqlite3
import pandas as pd

class AISDatabaseParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self.db = {}
        self.db_cursor = {}
        self.connection_string = self.scope.settings["enc"]["ais"]["connection_string"]
        self.start_db_connection()

    def get_ships(self) -> list[tuple]:
        ship_list = self.read_ships()
        transformed_ships = [self.transform_ship(ship) for ship in ship_list]
        return transformed_ships

    def start_db_connection(self)->None:
        self.db = sqlite3.connect(self.connection_string)
        self.cursor = self.db.cursor()
        print("db connected")

        self.get_newest_data()
    

    def get_newest_data(self) -> None:
        self.get_db_data(self.scope.settings["enc"]["time"]["time_end"])
    
    def get_db_data(self, timestamp) -> None:
        #time_end = datetime.strptime(slider_time_end_val, "%d-%m-%Y %H:%M")

        query = """
                SELECT t.mmsi, t.latitude, t.longtitude, t.heading, t.color, t.timestamp
                FROM AisHistory t
                JOIN (
                        SELECT mmsi, 
                        MAX(timestamp) AS max_timestamp
                        FROM AisHistory
                        WHERE timestamp <= :time_end
                        GROUP BY mmsi
                ) grouped_t ON t.mmsi = grouped_t.mmsi AND t.timestamp = grouped_t.max_timestamp;

                """

        df = pd.read_sql_query(query, self.db, params={"time_end": timestamp})
        print(df)

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
