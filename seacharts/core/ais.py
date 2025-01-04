import threading
from seacharts.core import Scope
from seacharts.core.aisShipData import AISShipData
from enum import Enum

class AISParser:
    scope: Scope
    ships_info: list[AISShipData] = []
    ships_list_lock: threading.Lock

    def __init__(self, scope: Scope):
        self.scope = scope
        self.ships_list_lock = threading.Lock()
        if self.scope.settings["enc"]["ais"].get("dynamic_scale") == True:
            self._dynamic_scale = True
        else:
            self._dynamic_scale = False
        self._user_scale = 1.0 if self.scope.settings["enc"]["ais"].get("scale") is None else self.scope.settings["enc"]["ais"]["scale"]
            
    def convert_to_utm(self, x: float, y: float) -> tuple[int, int]:
        if not self.validate_lon_lat(x, y):
            return (0, 0)
        try:
            return self.scope.extent.convert_lat_lon_to_utm(y, x)
        except OverflowError:
            return(0,0)
    
    def validate_lon_lat(self, lon: float, lat: float) -> bool:
        if -180 <= lon <= 180 and -90 <= lat <= 90:
            return True
        return False
    
    def get_ships(self) -> list[list]:
        return self.read_ships()
    
    def read_ships(self) -> list[list]:
        ships = []
        not_rendered_cnt = 0
        with self.ships_list_lock:
            for row in self.ships_info:
                if row.lat == None or row.lon == None:
                    continue
                
                transformed_row = self.transform_ship(row)
                
                if transformed_row == (-1,-1,-1,-1,""):
                    not_rendered_cnt+=1
                    continue
                ships.append(transformed_row)
        if self.scope.settings["enc"].get("ais", {}).get("module") == "db":
            print(f"not rendered ships: {not_rendered_cnt}\n")
        return ships
    
    
    def transform_ship(self, ship: AISShipData) -> tuple:
        try:
            mmsi = ship.mmsi
            if(self.scope.settings["enc"]["ais"]["coords_type"] == "lonlat"):
                lon,lat = self.convert_to_utm(ship.lon, ship.lat)
            else:
                lat = float(ship.lat)
                lon = float(ship.lon)
            if not self.scope.extent.is_in_bounding_box(lon,lat):
                return (-1,-1,-1,-1,"")
            heading = float(ship.heading) if ship.heading != '' and ship.heading != None else 511
            heading = heading if heading <= 360 else 511 
            color = ship.color
            if(type(ship.to_bow) is int and ship.to_bow is not None):
                scale = self.calculate_scale({"to_bow": ship.to_bow,"to_stern":ship.to_stern,"to_port":ship.to_port,"to_starboard":ship.to_starboard})
                return (mmsi, int(lon), int(lat), heading, color,scale)
        except Exception as e:
            return (-1,-1,-1,-1,"")
        return (mmsi, int(lon), int(lat), heading, color, self._user_scale)
    
    def get_ship_by_mmsi(self,mmsi: str) -> AISShipData:
        return next((ship for ship in self.ships_info if str(ship.mmsi) == str(mmsi)), None)
    
    @staticmethod
    def color_resolver(msg):
        if msg is None:
            return "DEFAULT"
        if isinstance(msg,str):
            return msg
        
        msg = int(msg)
        if msg == ShipType.DEFAULT.value:
            return  'DEFAULT' 
        elif 1 <= msg <= 19:
            return  'DEFAULT'   
        elif msg == ShipType.WIG.value:
            return  'WIG' 
        elif msg == ShipType.WIG_A.value:
            return  'WIG_A' 
        elif msg == ShipType.WIG_B.value:
            return  'WIG_B' 
        elif msg == ShipType.WIG_C.value:
            return  'WIG_C' 
        elif msg == ShipType.WIG_D.value:
            return  'WIG_D' 
        elif 25 <= msg <= 29:
            return  'WIG'
        elif msg == ShipType.FISHING.value:
            return  'FISHING' 
        elif msg == ShipType.TOWING.value:
            return  'TOWING' 
        elif msg == ShipType.TOWING_EXCEED.value:
            return  'TOWING_EXCEED' 
        elif msg == ShipType.DREDGING_UNDERWATER.value:
            return  'DREDGING_UNDERWATER' 
        elif msg == ShipType.DIVING_OPS.value:
            return  'DIVING_OPS' 
        elif msg == ShipType.MILITARY_OPS.value:
            return  'MILITARY_OPS' 
        elif msg == ShipType.SAILING.value:
            return  'SAILING' 
        elif msg == ShipType.PLEASURE_CRAFT.value:
            return  'PLEASURE_CRAFT' 
        elif 38 <= msg <= 39:
            return  'DEFAULT'  
        elif msg == ShipType.HSC.value:
            return  'HSC' 
        elif msg == ShipType.HSC_A.value:
            return  'HSC_A' 
        elif msg == ShipType.HSC_B.value:
            return  'HSC_B' 
        elif msg == ShipType.HSC_C.value:
            return  'HSC_C' 
        elif msg == ShipType.HSC_D.value:
            return  'HSC_D' 
        elif 45 <= msg <= 49:
            return  'HSC'   
        elif msg == ShipType.PILOT.value:
            return  'PILOT' 
        elif msg == ShipType.RESCUE.value:
            return  'RESCUE' 
        elif msg == ShipType.TUG.value:
            return  'TUG' 
        elif msg == ShipType.PORT_TENDER.value:
            return  'PORT_TENDER' 
        elif msg == ShipType.ANTI_POLLUTION_EQ.value:
            return  'ANTI_POLLUTION_EQ' 
        elif msg == ShipType.LAW_ENFORCEMENT.value:
            return  'LAW_ENFORCEMENT' 
        elif 56 <= msg <= 57:
            return  'LOCAL_VESSEL'   
        elif msg == ShipType.MEDICAL_TRANSPORT.value:
            return  'MEDICAL_TRANSPORT' 
        elif msg == ShipType.NONCOMBATANT.value:
            return  'NONCOMBATANT' 
        elif msg == ShipType.PASSENGER.value:
            return  'PASSENGER' 
        elif msg == ShipType.PASSENGER_A.value:
            return  'PASSENGER_A' 
        elif msg == ShipType.PASSENGER_B.value:
            return  'PASSENGER_B' 
        elif msg == ShipType.PASSENGER_C.value:
            return  'PASSENGER_C' 
        elif msg == ShipType.PASSENGER_D.value:
            return  'PASSENGER_D' 
        elif 65 <= msg <= 68:
            return  'PASSENGER'   
        elif msg == ShipType.CARGO.value:
            return  'CARGO'  
        elif msg == ShipType.CARGO_A.value:
            return  'CARGO' 
        elif msg == ShipType.CARGO_B.value:
            return  'CARGO_A' 
        elif msg == ShipType.CARGO_C.value:
            return  'CARGO_B' 
        elif msg == ShipType.CARGO_D.value:
            return  'CARGO_C' 
        elif msg == ShipType.CARGO_D.value:
            return  'CARGO_D' 
        elif 75 <= msg <= 78:
            return  'CARGO'  
        elif msg == ShipType.TANKER.value:
            return  'TANKER'  
        elif msg == ShipType.TANKER_A.value:
            return  'TANKER' 
        elif msg == ShipType.TANKER_B.value:
            return  'TANKER_A' 
        elif msg == ShipType.TANKER_C.value:
            return  'TANKER_B' 
        elif msg == ShipType.TANKER_D.value:
            return  'TANKER_C' 
        elif msg == ShipType.TANKER_D.value:
            return  'TANKER_D' 
        elif 85 <= msg <= 89:
            return  'TANKER'    
        elif msg == ShipType.OTHER.value:
            return  'OTHER' 
        elif msg == ShipType.OTHER_A.value:
            return  'OTHER_A' 
        elif msg == ShipType.OTHER_B.value:
            return  'OTHER_B' 
        elif msg == ShipType.OTHER_C.value:
            return  'OTHER_C' 
        elif msg == ShipType.OTHER_D.value:
            return  'OTHER_D' 
        elif 95 <= msg <= 99:
            return  'OTHER'  
        else:
            return  'DEFAULT' 

    
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
        return scale_factor

class ShipType(Enum):
    DEFAULT = 0
    WIG = 20
    WIG_A = 21
    WIG_B = 22
    WIG_C = 23
    WIG_D = 24
    FISHING = 30
    TOWING = 31
    TOWING_EXCEED = 32
    DREDGING_UNDERWATER = 33
    DIVING_OPS = 34
    MILITARY_OPS = 35
    SAILING = 36
    PLEASURE_CRAFT = 37
    HSC = 40
    HSC_A = 41
    HSC_B = 42
    HSC_C = 43
    HSC_D = 44
    PILOT = 50
    RESCUE = 51
    TUG = 52
    PORT_TENDER = 53
    ANTI_POLLUTION_EQ = 54
    LAW_ENFORCEMENT = 55
    LOCAL_VESSEL = 56
    MEDICAL_TRANSPORT = 58
    NONCOMBATANT = 59
    PASSENGER = 60
    PASSENGER_A = 61
    PASSENGER_B = 62
    PASSENGER_C = 63
    PASSENGER_D = 64
    CARGO = 70
    CARGO_A = 71
    CARGO_B = 72
    CARGO_C = 73
    CARGO_D = 74
    TANKER = 80
    TANKER_A = 81
    TANKER_B = 82
    TANKER_C = 83
    TANKER_D = 84
    OTHER = 90
    OTHER_A = 91
    OTHER_B = 92
    OTHER_C = 93
    OTHER_D = 94