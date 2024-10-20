from seacharts.core import AISParser, Scope
from seacharts.core.aisShipData import AISShipData
#from seacharts.display.colors import _ship_colors
from random import random
from datetime import datetime
import sqlite3
import pandas as pd
import csv
from datetime import datetime, timedelta
import threading
class AISDatabaseParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self._db = {}
        self._db_cursor = {}
        self._connection_string = self.scope.settings["enc"]["ais"]["connection_string"]
        self.db_column_names = {
            "mmsi": "mmsi",             
            "lon": "longtitude",               
            "lat": "latitude",               
            "last_updated": "last_updated",             
        }
        self.append_custom_column_names()
        self.ships_list_lock = threading.Lock()
        self.ships_info:list[AISShipData] = []
        if self.scope.settings["enc"]["ais"].get("dynamic_scale") == True:
            self._dynamic_scale = True
        else:
            self._dynamic_scale = False
        self._user_scale = 1.0 if self.scope.settings["enc"]["ais"].get("scale") is None else self.scope.settings["enc"]["ais"]["scale"]
        self._start_db_connection()


    def _start_db_connection(self)->None:
        """
        Starts the database connection based on connection string from config.yml
        """
        try:
            self._db = sqlite3.connect(self._connection_string)
            self.cursor = self._db.cursor()
            print("db connected")
        except sqlite3.Error as error:
            raise ValueError(f"Unable to connect to database \n{error}") from None

        self.get_start_data()
    

    def get_start_data(self) -> None:
        """
        Retrieves vessels' data corresponding to 'time_start' variable from config 
        (first value of slider at startup)
        """
        self.get_db_data(datetime.strptime(self.scope.settings["enc"]["time"]["time_start"],"%d-%m-%Y %H:%M"))
    
    def get_db_data(self, timestamp:datetime) -> list[tuple]:
        self.ships_info.clear()
        """
        Retrieves vessels' data based on passed timestamp
        
        :param datetime timestamp: The timestamp based on which vessels will be retrieved,  period (timestamp - [1*period type from config(min,hours)]) to timestamp
        :return: list of ships from the period
        :rtype: list[tuple]
        """
        print(timestamp)
        time_start,time_end = self._resolve_timestamp(timestamp)

        #time_end = datetime.strptime(slider_time_end_val, "%d-%m-%Y %H:%M")
        query= f"""
                SELECT {', '.join(f't.{custom}' for default, custom in self.db_column_names.items())}
                FROM AisHistory t
                JOIN (
                        SELECT {self.db_column_names["mmsi"]}, 
                        MAX({self.db_column_names["last_updated"]}) AS max_{self.db_column_names["last_updated"]}
                        FROM AisHistory
                        WHERE {self.db_column_names["last_updated"]} >= :time_start AND {self.db_column_names["last_updated"]} <= :time_end
                        GROUP BY {self.db_column_names["mmsi"]}
                ) grouped_t ON t.{self.db_column_names["mmsi"]} = grouped_t.{self.db_column_names["mmsi"]} AND t.{self.db_column_names["last_updated"]} = grouped_t.max_{self.db_column_names["last_updated"]};

                """
        
        print(query)
        
        try:
            df = pd.read_sql_query(query, self._db, params={"time_start":time_start,"time_end": time_end})
            print(df)
        except pd.errors.DatabaseError as error:
            raise ValueError(f"Unable to perform a query \n{error}") from None

        for index,col in df.iterrows():
                self.ships_info.append(AISDbShipData(col))
        return self.get_ships()

        # with open('data.csv', 'w', newline='') as f:
        #     fieldnames = ['mmsi', 'long', 'lat', 'heading', 'color']
        #     writer = csv.DictWriter(f, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for index, col in df.iterrows():

        #         writer.writerow({'mmsi': col["mmsi"], 'long': col["longtitude"], 'lat': col["latitude"], 'heading': col["heading"], 'color': col["color"]})
        # return self.get_ships()
        
    def _resolve_timestamp(self,timestamp:datetime) -> tuple[datetime,datetime]:
        """
        Find date a period (from config) before the given timestamp, the month is treated as 30 days, the year is treated as 365 days

        :param datetime timestamp: timestamp base from which the other date will be found, use hour period if not given in config
        :return: tuple of resolved dates
        :rtype: tuple[datetime,datetime]
        """
        time_end = timestamp.strftime("%d-%m-%Y %H:%M:%S")
        
        match self.scope.settings["enc"]["time"]["period"]:
            case "hour":
                time_start = (timestamp - timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")
            case "day":
                time_start = (timestamp - timedelta(days=1)).strftime("%d-%m-%Y %H:%M:%S")
            case "week":
                time_start = (timestamp - timedelta(weeks=1)).strftime("%d-%m-%Y %H:%M:%S")
            case "month":
                time_start = (timestamp - timedelta(days=30)).strftime("%d-%m-%Y %H:%M:%S")
            case "year":
                time_start = (timestamp - timedelta(days=365)).strftime("%d-%m-%Y %H:%M:%S")
            case _:
                time_start = (timestamp - timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")

        

        print(time_start)
        print(time_end)

        return time_start,time_end
    
    def append_custom_column_names(self):
        columns = self.scope.settings["enc"]["ais"].get("db_fields")
        if columns is None:
            return
        
        if "mmsi" in columns:
            self.db_column_names["mmsi"] = columns["mmsi"]
            del columns["mmsi"]

        if "lon" in columns:
            self.db_column_names["lon"] = columns["lon"]
            del columns["lon"]

        if "lat" in columns:
            self.db_column_names["lat"] = columns["lat"]
            del columns["lat"]

        if "last_updated" in columns:
            self.db_column_names["last_updated"] = columns["last_updated"]
            del columns["last_updated"]

        for key,val in columns.items():
            self.db_column_names[key] = val




    
class AISDbShipData(AISShipData):
    def __init__(self, col: pd.Series):
        self.mmsi = col.get("mmsi")
        self.lon = col.get("longtitude")
        self.lat = col.get("latitude")
        self.turn = col.get("turn")
        self.ship_type = col.get("ship_type")
        self.last_updated = col.get("timestamp")
        self.name = col.get("name")
        self.ais_version = col.get("ais_version")
        self.ais_type = col.get("ais_type")
        self.status = col.get("status")
        self.course = col.get("course")
        self.speed = col.get("speed")
        self.heading = col.get("heading")
        self.imo = col.get("imo")
        self.callsign = col.get("callsign")
        self.shipname = col.get("shipname")
        self.to_bow = col.get("to_bow")
        self.to_stern = col.get("to_stern")
        self.to_port = col.get("to_port")
        self.to_starboard = col.get("to_starboard")
        self.destination = col.get("destination")
        self.color = col.get("color") or AISParser.color_resolver(col.get("ship_type"))
    


    