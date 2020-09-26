
from math import pi

spider = {
    "mdh": [
        {"alpha": 0,  "a": 0, "theta": 0, "d": 0, "type": 1},
        {"alpha": pi/2, "a": 52, "theta": 0, "d": 0, "type": 1},
        {"alpha": 0, "a": 89, "theta": 0, "d": 0, "type": 1},
        {"alpha": 0, "a": 90, "theta": 0, "d": 0, "type": 1}
    ],
    # feet are arranged CCW, only spec (x,y)
    "neutral": [
        [100, 0],  # foot 1
        [100, 0],
        [100, 0],
        [100, 0],
        [100, 0],
        [100, 0]   # foot 6
    ],
    "forward": [
        []
    ],
    "back": [
        []
    ],
    "height": 50, # height above the floor, so this will be negative
}
