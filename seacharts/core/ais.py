from seacharts.core import Scope
from seacharts.core.aisShipData import AISShipData

class AISParser:
    scope: Scope
    ships_info: list[AISShipData] = []

    def __init__(self, scope: Scope):
        self.scope = scope
        if self.scope.settings["enc"]["ais"].get("dynamic_scale") == True:
            self._dynamic_scale = True
        else:
            self._dynamic_scale = False
        self._user_scale = 1.0 if self.scope.settings["enc"]["ais"].get("scale") is None else self.scope.settings["enc"]["ais"]["scale"]
        

    def get_ships(self) -> list[tuple]:
        raise NotImplementedError
    
    def convert_to_utm(self, x: float, y: float) -> tuple[int, int]:
        if not self.validate_lon_lat(x, y):
            return (0, 0)
        return self.scope.extent.convert_lat_lon_to_utm(x, y)
    
    def validate_lon_lat(self, lon: float, lat: float) -> bool:
        if -180 <= lon <= 180 and -90 <= lat <= 90:
            return True
        return False
    
    def get_ships(self) -> list[list]:
        return self.read_ships()
    
    def read_ships(self) -> list[list]:
        ships = []
        with self.ships_list_lock:
            for row in self.ships_info:
                if row.lat == None or row.lon == None:
                    continue
                
                transformed_row = self.transform_ship(row)
                
                if transformed_row == (-1,-1,-1,-1,""):
                    continue
                if not self.scope.extent.is_in_bounding_box(transformed_row[1],transformed_row[2]):
                    continue
                ships.append(transformed_row)
        return ships
    
    
    def transform_ship(self, ship: AISShipData) -> tuple:
        try:
            mmsi = ship.mmsi
            if(self.scope.settings["enc"]["ais"]["coords_type"] != "utm"):
                lat, lon = self.convert_to_utm(ship.lat, ship.lon)
            else:
                lat = float(ship.lat)
                lon = float(ship.lon)
            heading = float(ship.heading) if ship.heading != '' and ship.heading != None else 0
            heading = heading if heading <= 360 else 0 
            color = ship.color
            if(ship.to_bow is not None):
                scale = AISParser.calculate_scale({"to_bow": ship.to_bow,"to_stern":ship.to_stern,"to_port":ship.to_port,"to_starboard":ship.to_starboard})
                return (mmsi, int(lat), int(lon), heading, color,scale)
        except:
            return (-1,-1,-1,-1,"")
        return (mmsi, int(lat), int(lon), heading, color, 1.0 if not hasattr(self, '_user_scale') else self._user_scale)
    
    def get_ship_by_mmsi(self,mmsi: str) -> AISShipData:
        return next((ship for ship in self.ships_info if str(ship.mmsi) == str(mmsi)), None)
    
    @staticmethod
    def color_resolver(msg):
        if msg is None:
            return "default"
        if isinstance(msg,str):
            return msg
        
        msg = int(msg)
        if msg == 0:
            return  'default' 
        elif 1 <= msg <= 19:
            return  'default'   
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
            return  'WIG'
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
            return  'CARGO'  
        elif msg == 79:
            return  'CARGO'  
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
            return  'TANKER' 
        elif msg == 89:
            return  'TANKER'   
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
            return  'OTHER'  
        elif msg == 99:
            return  'OTHER'   
        else:
            return  'default' 

    
    def calculate_scale(self,ship_dimensions:dict):
        
        if self._dynamic_scale == False:
            return 1.0 if self._user_scale is None else self._user_scale

        avg_dimensions = {
            'to_bow': 30,
            'to_stern': 25,
            'to_port': 5,
            'to_starboard': 6
}
        total_ratio = 0
        
        for key in ship_dimensions.keys():
            if key in ship_dimensions:
                avg_value = avg_dimensions[key]
                actual_value = ship_dimensions[key]
                ratio = actual_value / avg_value
                total_ratio += ratio
        
        
        scale_factor = (total_ratio / len(ship_dimensions)) * self._user_scale if len(ship_dimensions) > 0 else 1.0
        print(f"Scale factor: {scale_factor}")
        return scale_factor
