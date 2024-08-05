import math
from seacharts.enc import ENC
from seacharts.core.extent import Extent
from pyproj import Transformer

enc = ENC("config.yaml")

print(enc.seabed[10])
print(enc.shore)
print(enc.land)
# ship = (1,612291 ,6071542,96,"red")
# ships = [tuple(ship), ]
# enc.display.add_vessels(*ships)
enc.display.show()