import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Note settings
NOTE_RADIUS = 20
NOTE_SPEED = 300  # pixels/sec
HIT_RADIUS = 30
HIT_Y = SCREEN_HEIGHT - 100
HIT_WINDOW = 30

# Lanes
num_lanes = 5
spacing = 60  # distance between each lane
start_x = SCREEN_WIDTH//2 - (spacing * (num_lanes-1))//2

LANE_X = {i: start_x + i*spacing for i in range(num_lanes)}


LANE_COLORS = {
    0: RED,
    1: GREEN,
    2: BLUE,
    3: YELLOW,
    4: PURPLE
}

# Key mapping for lanes
KEY_MAPPING = {
    0: "d",
    1: "f",
    2: "j",
    3: "k",
    4: "l"
}

# Hit scores
HIT_SCORES = {
    "Perfect": 100,
    "Good": 50,
    "Miss": 0
}
