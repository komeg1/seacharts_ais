import tkinter as tk
from tkinter import StringVar, font
from seacharts.core.aisShipData import AISShipData
class AISStaticInfoWindow:
    def __init__(self, root, ship_data):
        self.ship_data = ship_data
        self.root = root
        self.root.title(f"AIS Ship Data - {self.ship_data.shipname or 'Unknown'}")


        self.bold_font = font.Font(size=16, weight='bold')
        self.normal_font = font.Font(size=14)
        self.small_font = font.Font(size=12)
        
        self.no_vessel_message = tk.Label(self.root, text="Vessel AIS Static Information", font=self.bold_font)
        self.no_vessel_message.pack(pady=(20, 5)) 

        self.subtitle_var = StringVar(value="Click on a vessel to get more data")
        self.subtitle_label = tk.Label(self.root, textvariable=self.subtitle_var, font=self.normal_font)
        self.subtitle_label.pack(pady=(0, 20))

        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(pady=(20, 20))

        self.callsign_var = StringVar(value=f"Callsign: {self.ship_data.callsign}")
        self.lon_var = StringVar(value=f"Longitude: {self.ship_data.lon}")
        self.lat_var = StringVar(value=f"Latitude: {self.ship_data.lat}")
        self.turn_var = StringVar(value=f"Turn: {self.ship_data.turn}")
        self.speed_var = StringVar(value=f"Speed: {self.ship_data.speed}")
        self.course_var = StringVar(value=f"Course: {self.ship_data.course}")
        self.heading_var = StringVar(value=f"Heading: {self.ship_data.heading}")
        self.imo_var = StringVar(value=f"IMO: {self.ship_data.imo}")
        self.ship_type_var = StringVar(value=f"Ship Type: {self.ship_data.ship_type}")
        self.to_bow_var = StringVar(value=f"To Bow: {self.ship_data.to_bow}")
        self.to_stern_var = StringVar(value=f"To Stern: {self.ship_data.to_stern}")
        self.to_port_var = StringVar(value=f"To Port: {self.ship_data.to_port}")
        self.to_starboard_var = StringVar(value=f"To Starboard: {self.ship_data.to_starboard}")
        self.destination_var = StringVar(value=f"Destination: {self.ship_data.destination}")
        self.last_updated_var = StringVar(value=f"Last Updated: {self.ship_data.last_updated}")
        self.name_var = StringVar(value=f"Name: {self.ship_data.name}")
        self.ais_version_var = StringVar(value=f"AIS Version: {self.ship_data.ais_version}")
        self.ais_type_var = StringVar(value=f"AIS Type: {self.ship_data.ais_type}")
        self.status_var = StringVar(value=f"Status: {self.ship_data.status}")
        
        self.create_widgets()

    def create_widgets(self):
        labels = [
            self.callsign_var,
            self.lon_var,
            self.lat_var,
            self.turn_var,
            self.speed_var,
            self.course_var,
            self.heading_var,
            self.imo_var,
            self.ship_type_var,
            self.to_bow_var,
            self.to_stern_var,
            self.to_port_var,
            self.to_starboard_var,
            self.destination_var,
            self.last_updated_var,
            self.name_var,
            self.ais_version_var,
            self.ais_type_var,
            self.status_var,
        ]

        for var in labels:
            tk.Label(self.data_frame, textvariable=var, font=self.small_font, anchor="w").pack(fill='x')



    def update_data(self):
        if self.ship_data:
            self.root.title(f"AIS Ship Data - {self.ship_data.shipname or self.ship_data.mmsi or 'Unknown'}")
            self.subtitle_var.set(f"MMSI: {self.get_display_value(self.ship_data.mmsi)} | Name: {self.get_display_value(self.ship_data.shipname)}")

            self.callsign_var.set(f"Callsign: {self.get_display_value(self.ship_data.callsign)}")
            self.lon_var.set(f"Longitude: {self.get_display_value(self.ship_data.lon)}")
            self.lat_var.set(f"Latitude: {self.get_display_value(self.ship_data.lat)}")
            self.turn_var.set(f"Turn: {self.get_display_value(self.ship_data.turn)}")
            self.speed_var.set(f"Speed: {self.get_display_value(self.ship_data.speed)}")
            self.course_var.set(f"Course: {self.get_display_value(self.ship_data.course)}")
            self.heading_var.set(f"Heading: {self.get_display_value(self.ship_data.heading)}")
            self.imo_var.set(f"IMO: {self.get_display_value(self.ship_data.imo)}")
            self.ship_type_var.set(f"Ship Type: {'No data' if self.get_display_value(self.ship_data.color) == 'default' else self.get_display_value(self.ship_data.color)}")
            self.to_bow_var.set(f"To Bow: {self.get_display_value(self.ship_data.to_bow)}")
            self.to_stern_var.set(f"To Stern: {self.get_display_value(self.ship_data.to_stern)}")
            self.to_port_var.set(f"To Port: {self.get_display_value(self.ship_data.to_port)}")
            self.to_starboard_var.set(f"To Starboard: {self.get_display_value(self.ship_data.to_starboard)}")
            self.destination_var.set(f"Destination: {self.get_display_value(self.ship_data.destination)}")
            self.last_updated_var.set(f"Last Updated: {self.get_display_value(self.ship_data.last_updated)}")
            self.name_var.set(f"Name: {self.get_display_value(self.ship_data.name)}")
            self.ais_version_var.set(f"AIS Version: {self.get_display_value(self.ship_data.ais_version)}")
            self.ais_type_var.set(f"AIS Type: {self.get_display_value(self.ship_data.ais_type)}")
            self.status_var.set(f"Status: {self.get_display_value(self.ship_data.status)}")
        else:
            self.root.title("AIS Ship Data - No Vessel Selected")
            self.subtitle_var.set("Click on a vessel to get more data")

            self.mmsi_var.set("MMSI: No Data")
            self.shipname_var.set("Name: No Data")
            self.callsign_var.set("Callsign: No Data")
            self.lon_var.set("Longitude: No Data")
            self.lat_var.set("Latitude: No Data")
            self.turn_var.set("Turn: No Data")
            self.speed_var.set("Speed: No Data")
            self.course_var.set("Course: No Data")
            self.heading_var.set("Heading: No Data")
            self.imo_var.set("IMO: No Data")
            self.ship_type_var.set("Ship Type: No Data")
            self.to_bow_var.set("To Bow: No Data")
            self.to_stern_var.set("To Stern: No Data")
            self.to_port_var.set("To Port: No Data")
            self.to_starboard_var.set("To Starboard: No Data")
            self.destination_var.set("Destination: No Data")
            self.last_updated_var.set("Last Updated: No Data")
            self.name_var.set("Name: No Data")
            self.ais_version_var.set("AIS Version: No Data")
            self.ais_type_var.set("AIS Type: No Data")
            self.status_var.set("Status: No Data")
            self.color_var.set("Color: No Data")

    def get_display_value(self, value):
        """Return 'No Data' if the value is None, otherwise return the value."""
        return value if value is not None else "No Data"
       

    def refresh_data(self, new_ship_data:AISShipData):
        self.ship_data = new_ship_data
        self.update_data()