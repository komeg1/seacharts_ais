import requests
from pyais import decode
from pyais.stream import TCPConnection
from pyais import AISTracker
import threading
import time
import csv

host = '#'
port = 0



def listen_stream()->None:
    print("Listening to stream {host}:{port}")
    with AISTracker() as tracker:
        t = threading.Timer(30, get_current_data, [tracker])
        t.start()
        for msg in TCPConnection(host,port=port):
            decoded_message = msg.decode()
            ais_content = decoded_message
            tracker.update(msg)
        

def get_current_data(tracker: AISTracker)->None:
    print("saving data to csv")
    with open('data.csv', 'w') as f:
        fieldnames = ['mmsi', 'long', 'lat', 'heading', 'color']
        writer = csv.writer(f, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ship in tracker.tracks:
            writer.writerow({'mmsi': ship.mmsi, 'long': ship.lon, 'lat': ship.lat, 'heading': ship.heading, 'color': 'green'})

    timer = threading.Timer(30, get_current_data, [tracker])
    timer.start()
            


