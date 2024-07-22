import math
from seacharts.enc import ENC
from seacharts.core.extent import Extent
from pyproj import Transformer

def convert_lat_lon_to_utm(lat: float, lon: float):
    transformer = Transformer.from_crs("epsg:4326", "epsg:32633")
    coords = transformer.transform(lat, lon)
    utm_easting = math.ceil(coords[0])
    utm_northing = math.ceil(coords[1])
    return utm_easting, utm_northing


enc = ENC("config.yaml")

print(enc.seabed[10])
print(enc.shore)
print(enc.land)
ship = (1,600075,6055000,96,"red")
print(ship)
ships = [tuple(ship), ]
enc.display.add_vessels(*ships)
enc.display.show()