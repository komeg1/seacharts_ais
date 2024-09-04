import math
from seacharts.enc import ENC
from seacharts.core.extent import Extent
from pyproj import Transformer

enc = ENC("config.yaml")
# ships = [
#         (1, 612291, 6071542, 132, "orange"),
#         (2, 356393, 6052365, 57, "yellow")
#     ]

# enc.display.add_vessels(*ships)
# enc.display.start()

enc.display.show()