from seacharts.core import AISParser, Scope
#from seacharts.display.colors import _ship_colors
from random import random
from datetime import datetime
import sqlite3
import pandas as pd
import csv
from datetime import datetime, timedelta

class AISDatabaseParser(AISParser):
    def __init__(self, scope: Scope):
        self.scope = scope
        self._db = {}
        self._db_cursor = {}
        self._connection_string = self.scope.settings["enc"]["ais"]["connection_string"]
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
        """
        Retrieves vessels' data based on passed timestamp
        
        :param datetime timestamp: The timestamp based on which vessels will be retrieved,  period (timestamp - [1*period type from config(min,hours)]) to timestamp
        :return: list of ships from the period
        :rtype: list[tuple]
        """
        print(timestamp)
        time_start,time_end = self._resolve_timestamp(timestamp)

        #time_end = datetime.strptime(slider_time_end_val, "%d-%m-%Y %H:%M")

        query = """
                SELECT t.mmsi, t.latitude, t.longtitude, t.heading, t.color, t.timestamp
                FROM AisHistory t
                JOIN (
                        SELECT mmsi, 
                        MAX(timestamp) AS max_timestamp
                        FROM AisHistory
                        WHERE timestamp >= :time_start AND timestamp <= :time_end
                        GROUP BY mmsi
                ) grouped_t ON t.mmsi = grouped_t.mmsi AND t.timestamp = grouped_t.max_timestamp;

                """

        df = pd.read_sql_query(query, self._db, params={"time_start":time_start,"time_end": time_end})
        print(df)
        with open('data.csv', 'w', newline='') as f:
            fieldnames = ['mmsi', 'long', 'lat', 'heading', 'color']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for index, col in df.iterrows():
                writer.writerow({'mmsi': col["mmsi"], 'long': col["longtitude"], 'lat': col["latitude"], 'heading': col["heading"], 'color': col["color"]})
        return self.get_ships()
        
    def _resolve_timestamp(self,timestamp:datetime) -> tuple[datetime,datetime]:
        """
        Find a date a period (from config) before the given timestamp, the month is treated as 30 days, the year is treated as 365 days

        :param datetime timestamp: timestamp base from which the other date will be found, use hour period if not given in config
        :return: tuple of resolved dates
        :rtype: tuple[datetime,datetime]
        """
        time_end = timestamp.strftime("%d-%m-%Y %H:%M")
        
        match self.scope.settings["enc"]["time"]["period"]:
            case "hour":
                time_start = (timestamp - timedelta(hours=1)).strftime("%d-%m-%Y %H:%M")
            case "day":
                time_start = (timestamp - timedelta(days=1)).strftime("%d-%m-%Y %H:%M")
            case "week":
                time_start = (timestamp - timedelta(weeks=1)).strftime("%d-%m-%Y %H:%M")
            case "month":
                time_start = (timestamp - timedelta(days=30)).strftime("%d-%m-%Y %H:%M")
            case "year":
                time_start = (timestamp - timedelta(days=365)).strftime("%d-%m-%Y %H:%M")
            case _:
                time_start = (timestamp - timedelta(hours=1)).strftime("%d-%m-%Y %H:%M")

        

        print(time_start)
        print(time_end)

        return time_start,time_end


    
