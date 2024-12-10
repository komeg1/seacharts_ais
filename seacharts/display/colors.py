"""
Contains functions and structures for color management.
"""
import re

import matplotlib.colors as clr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar


def _blues(bins: int = 9) -> np.ndarray:
    return plt.get_cmap("Blues")(np.linspace(0.6, 1.0, bins))


def _greens(bins: int = 9) -> np.ndarray:
    return plt.get_cmap("Greens")(np.linspace(0.3, 0.9, bins))


_ship_colors = dict(
    red=("#ff0000", "#ff000055"),
    blue=("#0000ff", "#0000ff55"),
    green=("#00ff00", "#00ff0055"),
    yellow=("#ffff00", "#ffff0055"),
    cyan=("#00ffff", "#00ffff55"),
    magenta=("#ff00ff", "#ff00ff55"),
    pink=("#ff88ff", "#ff88ff55"),
    purple=("#bb22ff", "#bb22ff55"),
    orange=("#ff9900", "#ff990055"),
    white=("#ffffff", "#ffffff77"),
    lightgrey=("#b7b7b7", "#b7b7b755"),
    grey=("#666666", "#66666655"),
    darkgrey=("#333333", "#33333355"),
    black=("#000000", "#00000077"),
)

_vessel_colors = dict(
    DEFAULT              = ("#CCCCCC", "#CCCCCC55"),
    WIG                  = ("#FF5733", "#FF573355"),
    FISHING              = ("#FF8C00", "#FF8C0055"),
    TOWING               = ("#FFD700", "#FFD70055"),
    TOWING_EXCEED        = ("#FF4500", "#FF450055"),
    DREDGING_UNDERWATER  = ("#8A2BE2", "#8A2BE255"),
    DIVING_OPS           = ("#4682B4", "#4682B455"),
    MILITARY_OPS         = ("#696969", "#69696955"),
    SAILING              = ("#00FF7F", "#00FF7F55"),
    PLEASURE_CRAFT       = ("#FF69B4", "#FF69B455"),
    HSC                  = ("#4B0082", "#4B008255"),
    HSC_A                = ("#800080", "#80008055"),
    HSC_B                = ("#9370DB", "#9370DB55"),
    HSC_C                = ("#8B0000", "#8B000055"),
    HSC_D                = ("#B22222", "#B2222255"),
    PILOT                = ("#00008B", "#00008B55"),
    RESCUE               = ("#FF0000", "#FF000055"),
    TUG                  = ("#D2691E", "#D2691E55"),
    PORT_TENDER          = ("#8B4513", "#8B451355"),
    ANTI_POLLUTION_EQ    = ("#20B2AA", "#20B2AA55"),
    LAW_ENFORCEMENT      = ("#000080", "#00008055"),
    LOCAL_VESSEL         = ("#32CD32", "#32CD3255"),
    MEDICAL_TRANSPORT    = ("#FF6347", "#FF634755"),
    NONCOMBATANT         = ("#778899", "#77889955"),
    PASSENGER            = ("#1E90FF", "#1E90FF55"),
    PASSENGER_A          = ("#00CED1", "#00CED155"),
    PASSENGER_B          = ("#40E0D0", "#40E0D055"),
    PASSENGER_C          = ("#4682B4", "#4682B455"),
    PASSENGER_D          = ("#5F9EA0", "#5F9EA055"),
    CARGO                = ("#DAA520", "#DAA52055"),
    CARGO_A              = ("#B8860B", "#B8860B55"),
    CARGO_B              = ("#CD853F", "#CD853F55"),
    CARGO_C              = ("#D2B48C", "#D2B48C55"),
    CARGO_D              = ("#A0522D", "#A0522D55"),
    TANKER               = ("#FFFF00", "#FFFF0055"),
    TANKER_A             = ("#FF4500", "#FF450055"),
    TANKER_B             = ("#FF6347", "#FF634755"),
    TANKER_C             = ("#FFA07A", "#FFA07A55"),
    TANKER_D             = ("#FA8072", "#FA807255"),
    OTHER                = ("#696969", "#69696955"),
    OTHER_A              = ("#708090", "#70809055"),
    OTHER_B              = ("#778899", "#77889955"),
    OTHER_C              = ("#A9A9A9", "#A9A9A955"),
    OTHER_D              = ("#D3D3D3", "#D3D3D355")
)

_horizon_colors = dict(
    full_horizon=("#ffffff55", "#ffffff11"),
    starboard_bow=("#00ff0099", "#00ff0055"),
    starboard_side=("#33ff3399", "#33ff3355"),
    starboard_aft=("#ccffcc99", "#ccffcc55"),
    rear_aft=("#eeeeee99", "#eeeeee55"),
    port_aft=("#ffcccc99", "#ffcccc55"),
    port_side=("#ff333388", "#ff333355"),
    port_bow=("#ff000066", "#ff000055"),
)

_layer_colors = dict(
    Seabed=_blues()[0],
    Land=_greens()[4],
    Shore=_greens()[3],
    highlight=("#ffffff44", "#ffffff44"),
    blank=("#ffffffff", "#ffffffff"),
)

@staticmethod
def assign_custom_colors(colors:dict):
    for name,color in colors.items():
        if name in _vessel_colors:
            _vessel_colors[name] = (color,color + "55")
            print(_vessel_colors[name])

def color_picker(name: str, bins: int = None) -> tuple:
    #print(f"picked color {name}")
    if isinstance(name, int):
        return _blues(bins)[name]
    elif name in _vessel_colors:
        return _vessel_colors[name]
    elif name in _ship_colors:
        return _ship_colors[name]
    elif name in _horizon_colors:
        return _horizon_colors[name]
    elif name in _layer_colors:
        return _layer_colors[name]
    elif name in clr.CSS4_COLORS:
        return clr.CSS4_COLORS[name]
    elif re.match("^#(?:[0-9a-fA-F]{3,4}){1,2}$",name):
        return name,name
    else:
        raise ValueError(f"{name} is not a valid color")


def colorbar(axes: Axes, depths: list[int]) -> Colorbar:
    depths = list(depths)
    ocean = list(_blues(len(depths)))
    colors = [_layer_colors["Shore"]] + ocean[:-1]
    c_map = clr.LinearSegmentedColormap.from_list("Custom terrain", colors, len(colors))
    c_map.set_over(ocean[-1])
    c_map.set_under(_layer_colors["Land"])
    norm = clr.BoundaryNorm([0] + depths[1:], c_map.N)
    kwargs = dict(
        extend="both",
        use_gridspec=True,
        extendfrac=0.1,
        format="%1i m",
        ticks=[0, 1] + depths[1:],
        boundaries=([depths[0] - 100] + [0, 1] + depths[1:] + [depths[-1] + 100]),
    )
    mappable = ScalarMappable(norm=norm, cmap=c_map)
    cb = plt.colorbar(mappable, cax=axes, **kwargs)
    cb.ax.tick_params(labelsize=20, length=5, width=1.5)
    cb.outline.set_linewidth(1.5)
    cb.ax.invert_yaxis()
    return cb

