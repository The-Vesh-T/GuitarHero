import pygame
import sys
import time
from constants import *
from game import Game
import serial
import threading
import glob

fret_down = {
    "d": False,
    "f": False,
    "j": False,
    "k": False,
    "l": False
}

beat_recording = False
beat_times = []

song_start_time = None
SONG_LENGTH = 4 * 60 + 2   # 4:02


arduino_input = None
current_fret = None
strum_triggered = False

arduino_input = None

def read_arduino():
    global arduino_input

    # Auto-detect USB modem port
    port_list = glob.glob("/dev/tty.usbmodem*")
    if not port_list:
        print("ERROR: No Arduino found!")
        return

    ser = serial.Serial(port_list[0], 9600)
    print("Connected to Arduino on", port_list[0])

    while True:
        try:
            line = ser.readline().decode().strip()
            if line:
                arduino_input = line
        except:
            pass


# Start the thread
threading.Thread(target=read_arduino, daemon=True).start()

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero")
clock = pygame.time.Clock()

# --- Initialize mixer for music ---
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/Survivor - Eye Of The Tiger (Lyrics).mp3")
pygame.mixer.music.set_volume(0.7)  # adjust volume 0.0 - 1.0


# --- Fonts ---
font = pygame.font.SysFont("Consolas", 28)
big_font = pygame.font.SysFont("Consolas", 50, bold=True)
title_font = pygame.font.SysFont("Arial Black", 60, bold=True)

# --- Game object ---
game = Game()

# --- Notes chart ---
note_chart = [
    # --- INTRO HEARTBEAT (8 beats) ---
    {"time": 1.515, "key": "R"},
    {"time": 2.062, "key": "R"},
    {"time": 2.666, "key": "R"},
    {"time": 3.176, "key": "R"},
    {"time": 3.715, "key": "R"},
    {"time": 4.259, "key": "R"},
    {"time": 4.784, "key": "R"},
    {"time": 5.361, "key": "R"},
    {"time": 5.884, "key": "R"},
    {"time": 6.423, "key": "R"},
    {"time": 6.997, "key": "R"},
    {"time": 7.503, "key": "R"},
    {"time": 8.029, "key": "R"},
    {"time": 8.029, "key": "B"},
    {"time": 8.029, "key": "P"}, 

    {"time": 9.246, "key": "R"},
    {"time": 9.246, "key": "B"},
    {"time": 9.246, "key": "P"},

    {"time": 9.607, "key": "G"},
    {"time": 9.607, "key": "Y"},

    {"time": 9.992, "key": "R"},
    {"time": 9.992, "key": "B"},
    {"time": 9.992, "key": "P"},

    {"time": 11.236, "key": "R"},
    {"time": 11.236, "key": "P"},

    {"time": 11.708, "key": "G"}, #down
    {"time": 11.708, "key": "Y"},

    {"time": 12.166, "key": "R"},#UP
    {"time": 12.166, "key": "B"},
    {"time": 12.166, "key": "P"},

    {"time": 13.530, "key": "R"}, #up
    {"time": 13.530, "key": "B"},
    {"time": 13.530, "key": "P"},

    {"time": 13.970, "key": "G"}, #down
    {"time": 13.970, "key": "Y"},

    {"time": 14.409, "key": "B"}, #double down
    {"time": 14.409, "key": "Y"},
    {"time": 14.409, "key": "P"},

    {"time": 17.075, "key": "R"}, #up
    {"time": 17.075, "key": "B"},
    {"time": 17.075, "key": "P"},

    {"time": 18.014, "key": "R"}, #up
    {"time": 18.014, "key": "B"},
    {"time": 18.014, "key": "P"},

    {"time": 18.432, "key": "G"}, #down
    {"time": 18.432, "key": "Y"},

    {"time": 18.818, "key": "R"}, #up
    {"time": 18.818, "key": "B"},
    {"time": 18.818, "key": "P"},

    {"time": 20.306, "key": "R"}, #up
    {"time": 20.306, "key": "B"},
    {"time": 20.306, "key": "P"},

    {"time": 20.844, "key": "G"}, #down
    {"time": 20.844, "key": "Y"},

    {"time": 21.267, "key": "R"}, #up
    {"time": 21.267, "key": "B"},
    {"time": 21.267, "key": "P"},

    {"time": 22.589, "key": "R"}, #up
    {"time": 22.589, "key": "B"},
    {"time": 22.589, "key": "P"},

    {"time": 22.840, "key": "G"}, #down
    {"time": 22.840, "key": "Y"},

    {"time": 23.248, "key": "B"}, #double down
    {"time": 23.248, "key": "Y"},
    {"time": 23.248, "key": "P"},

    {"time": 25.855, "key": "P"}, 
    {"time": 26.270, "key": "Y"},
    {"time": 26.840, "key": "P"}, 
    {"time": 27.396, "key": "Y"}, 
    {"time": 27.986, "key": "P"},
    {"time": 28.544, "key": "Y"},
    {"time": 29.109, "key": "P"},
    {"time": 29.647, "key": "Y"},
    {"time": 30.204, "key": "P"},
    {"time": 30.760, "key": "Y"},
    {"time": 31.313, "key": "P"},
    {"time": 31.820, "key": "Y"},
    {"time": 32.361, "key": "P"},
    {"time": 32.912, "key": "Y"},
    {"time": 33.450, "key": "P"},

    #Back to guitar notes
    {"time": 25.818, "key": "B"},

    {"time": 26.872, "key": "R"},
    {"time": 26.872, "key": "G"},

    {"time": 27.292, "key": "B"},

    {"time": 27.697, "key": "R"},
    {"time": 27.697, "key": "G"},

    {"time": 29.081, "key": "R"},
    {"time": 29.081, "key": "G"},

    {"time": 29.486, "key": "B"},

    {"time": 29.875, "key": "R"},
    {"time": 29.875, "key": "G"},

    {"time": 31.255, "key": "G"},
    {"time": 31.678, "key": "B"},
    {"time": 32.084, "key": "R"},

##
    {"time": 34.565, "key": "B"},

    {"time": 35.712, "key": "R"},
    {"time": 35.712, "key": "G"},

    {"time": 36.120, "key": "B"},

    {"time": 36.479, "key": "R"},
    {"time": 36.479, "key": "G"},

    {"time": 37.865, "key": "R"},
    {"time": 37.865, "key": "G"},

    {"time": 38.302, "key": "B"},

    {"time": 38.706, "key": "R"},
    {"time": 38.706, "key": "G"},

    {"time": 40.137, "key": "G"},
    {"time": 40.561, "key": "B"},
    {"time": 40.967, "key": "R"},


    #Chord before start
    {"time": 43.400, "key": "R"},
    {"time": 43.400, "key": "B"},
    {"time": 43.400, "key": "P"},
    #down time
    {"time": 43.990, "key": "R"},
    {"time": 44.521, "key": "R"},
    {"time": 45.086, "key": "R"},
    {"time": 45.609, "key": "R"},
    {"time": 46.178, "key": "R"},
    {"time": 46.701, "key": "R"},
    {"time": 47.188, "key": "B"},
    {"time": 47.298, "key": "R"},
    {"time": 47.497, "key": "G"},
    {"time": 47.823, "key": "R"},

    #Chill song part
    {"time": 48.444, "key": "R"},
    {"time": 48.941, "key": "B"},
    {"time": 49.555, "key": "R"},
    {"time": 50.052, "key": "B"},
    {"time": 50.052, "key": "Y"},
    {"time": 50.629, "key": "R"},
    {"time": 51.141, "key": "B"},
    {"time": 51.723, "key": "R"},
    {"time": 52.239, "key": "B"},
    {"time": 52.239, "key": "Y"},
    {"time": 52.847, "key": "R"},
    {"time": 53.339, "key": "B"},
    {"time": 53.914, "key": "R"},
    {"time": 54.422, "key": "B"},
    {"time": 54.422, "key": "Y"},
    {"time": 54.961, "key": "R"},
    {"time": 55.493, "key": "B"},
    {"time": 56.076, "key": "R"},
    {"time": 56.633, "key": "B"},
    {"time": 56.633, "key": "Y"},
    {"time": 57.188, "key": "R"},
    {"time": 57.763, "key": "B"},
    {"time": 58.312, "key": "R"},
    {"time": 58.858, "key": "B"},
    {"time": 58.858, "key": "Y"},
    {"time": 59.437, "key": "R"},
    {"time": 59.957, "key": "B"},
    {"time": 60.569, "key": "R"},
    {"time": 61.072, "key": "B"},
    {"time": 61.072, "key": "Y"},
    {"time": 61.631, "key": "R"},
    {"time": 62.138, "key": "B"},
    {"time": 62.709, "key": "R"},
    {"time": 63.253, "key": "B"},
    {"time": 63.253, "key": "Y"},
    {"time": 64.658, "key": "R"},
    {"time": 65.026, "key": "B"},
    {"time": 65.414, "key": "R"},
    {"time": 65.414, "key": "Y"},
    {"time": 65.987, "key": "B"},
    {"time": 66.543, "key": "R"},
    {"time": 67.114, "key": "B"},
    {"time": 67.655, "key": "R"},
    {"time": 67.655, "key": "Y"},
    {"time": 68.739, "key": "B"},
    {"time": 69.278, "key": "R"},
    {"time": 69.851, "key": "B"},
    {"time": 69.851, "key": "Y"},
    {"time": 70.437, "key": "R"},
    {"time": 70.959, "key": "B"},
    {"time": 71.515, "key": "R"},
    {"time": 72.071, "key": "B"},
    {"time": 72.071, "key": "Y"},
    {"time": 72.658, "key": "R"},
    {"time": 73.179, "key": "B"},
    {"time": 73.737, "key": "R"},
    {"time": 74.256, "key": "B"},
    {"time": 74.256, "key": "Y"},
    {"time": 74.848, "key": "R"},
    {"time": 75.387, "key": "B"},
    {"time": 75.967, "key": "R"},
    {"time": 76.512, "key": "B"},
    {"time": 76.512, "key": "Y"},
    {"time": 77.103, "key": "R"},
    {"time": 77.624, "key": "B"},
    {"time": 78.181, "key": "R"},
    {"time": 78.706, "key": "B"},
    {"time": 78.706, "key": "Y"},
    {"time": 79.349, "key": "R"},
    {"time": 79.823, "key": "B"},
    {"time": 80.378, "key": "R"},
    {"time": 80.900, "key": "B"},
    {"time": 80.900, "key": "Y"},

    {"time": 82.633, "key": "P"},
    {"time": 82.919, "key": "B"},
    {"time": 83.307, "key": "R"},
    {"time": 85.469, "key": "P"},
    {"time": 85.469, "key": "B"},
    {"time": 86.414, "key": "R"},
    {"time": 87.052, "key": "B"},
    {"time": 87.289, "key": "Y"},
    {"time": 87.289, "key": "R"},
    {"time": 87.626, "key": "G"},
    {"time": 89.873, "key": "P"},
    {"time": 89.873, "key": "R"},
    {"time": 90.179, "key": "Y"},
    {"time": 90.179, "key": "G"},
    {"time": 91.312, "key": "R"},
    {"time": 91.312, "key": "B"},
    {"time": 91.618, "key": "P"},
    {"time": 92.060, "key": "B"},
    {"time": 93.929, "key": "R"},
    {"time": 95.420, "key": "P"},
    {"time": 96.114, "key": "B"},
    {"time": 96.537, "key": "R"},
    {"time": 96.956, "key": "Y"},
    {"time": 97.276, "key": "G"},
    {"time": 97.564, "key": "P"},
    {"time": 97.564, "key": "B"},
    {"time": 97.903, "key": "R"},
    {"time": 98.256, "key": "Y"},
    {"time": 98.611, "key": "G"},
    {"time": 101.179, "key": "P"},
    {"time": 101.179, "key": "R"},

    #Second
    {"time": 102.131, "key": "P"},
    {"time": 102.568, "key": "B"},
    {"time": 103.106, "key": "P"},
    {"time": 103.599, "key": "B"},
    {"time": 104.192, "key": "P"},
    {"time": 104.718, "key": "B"},
    {"time": 105.277, "key": "P"},
    {"time": 105.850, "key": "B"},
    {"time": 106.375, "key": "P"},
    {"time": 106.932, "key": "B"},
    {"time": 107.520, "key": "P"},
    {"time": 108.046, "key": "B"},
    {"time": 108.554, "key": "P"},
    {"time": 109.096, "key": "B"},
    {"time": 109.573, "key": "P"},
    {"time": 110.210, "key": "B"},
    {"time": 110.785, "key": "P"},
    {"time": 111.360, "key": "B"},
    {"time": 111.901, "key": "P"},
    {"time": 112.460, "key": "B"},
    {"time": 113.001, "key": "P"},
    {"time": 113.594, "key": "B"},

    {"time": 107.520, "key": "R"}, 
    {"time": 108.759, "key": "Y"},   
    {"time": 109.573, "key": "G"},   
    {"time": 113.231, "key": "R"},   
    {"time": 113.416, "key": "Y"},   
    {"time": 113.835, "key": "G"},   


    {"time": 114.151, "key": "P"},
    {"time": 114.694, "key": "B"},
    {"time": 115.252, "key": "P"},
    {"time": 115.840, "key": "B"},
    {"time": 116.365, "key": "P"},
    {"time": 116.365, "key": "G"},
    {"time": 116.856, "key": "B"},
    {"time": 117.462, "key": "P"},
    {"time": 117.954, "key": "B"},
    {"time": 118.515, "key": "P"},
    {"time": 119.037, "key": "B"},
    {"time": 119.609, "key": "P"},
    {"time": 120.113, "key": "B"},
    {"time": 120.638, "key": "P"},
    {"time": 120.638, "key": "G"},
    {"time": 121.163, "key": "B"},
    {"time": 121.740, "key": "P"},
    {"time": 122.330, "key": "B"},
    {"time": 122.904, "key": "P"},

    {"time": 125.021, "key": "G"},

    {"time": 126.181, "key": "R"},
    {"time": 126.181, "key": "G"},

    {"time": 127.254, "key": "B"},

    {"time": 129.418, "key": "P"},
    {"time": 129.418, "key": "G"},

    {"time": 129.962, "key": "Y"},

    {"time": 130.965, "key": "R"},
    {"time": 130.965, "key": "B"},
    {"time": 130.965, "key": "G"},

    {"time": 131.320, "key": "P"},

    {"time": 131.636, "key": "G"},
    {"time": 131.636, "key": "R"},

    {"time": 133.828, "key": "R"},

    {"time": 134.966, "key": "B"},
    {"time": 134.966, "key": "G"},

    {"time": 135.530, "key": "G"},

    {"time": 135.805, "key": "B"},
    {"time": 135.805, "key": "G"},

    {"time": 136.042, "key": "P"},

    {"time": 136.836, "key": "Y"},
    {"time": 136.836, "key": "G"},

    {"time": 137.125, "key": "B"},

    {"time": 137.527, "key": "G"},
    {"time": 137.527, "key": "R"},

    {"time": 138.216, "key": "R"},

    {"time": 140.394, "key": "P"},
    {"time": 140.394, "key": "G"},

    {"time": 145.152, "key": "B"},
    {"time": 145.152, "key": "P"},
    {"time": 145.595, "key": "Y"},
    {"time": 146.177, "key": "B"},
    {"time": 146.177, "key": "P"},
    {"time": 146.731, "key": "Y"},
    {"time": 147.255, "key": "B"},
    {"time": 147.255, "key": "P"},
    {"time": 147.823, "key": "Y"},
    {"time": 148.439, "key": "B"},
    {"time": 148.439, "key": "P"},
    {"time": 148.936, "key": "Y"},
    {"time": 149.490, "key": "B"},
    {"time": 149.490, "key": "P"},
    {"time": 150.074, "key": "Y"},
    {"time": 151.718, "key": "B"},
    {"time": 151.718, "key": "P"},
    {"time": 152.747, "key": "G"},
    {"time": 153.794, "key": "B"},
    {"time": 153.794, "key": "P"},
    {"time": 154.996, "key": "G"},

    {"time": 156.100, "key": "G"},
    {"time": 157.444, "key": "Y"},
    {"time": 157.444, "key": "P"},
    {"time": 157.595, "key": "Y"},
    {"time": 157.595, "key": "P"},
    {"time": 157.776, "key": "G"},
    {"time": 159.482, "key": "G"},
    {"time": 160.556, "key": "G"},
    {"time": 161.616, "key": "G"},

    {"time": 162.158, "key": "B"},
    {"time": 162.665, "key": "G"},
    {"time": 162.665, "key": "R"},

    {"time": 163.238, "key": "B"},
    {"time": 163.793, "key": "G"},
    {"time": 163.793, "key": "R"},

    {"time": 164.286, "key": "B"},
    {"time": 164.858, "key": "G"},
    {"time": 164.858, "key": "R"},

    {"time": 165.366, "key": "B"},
    {"time": 165.859, "key": "B"},
    {"time": 165.960, "key": "G"},

    {"time": 166.516, "key": "B"},
    

    {"time": 167.174, "key": "P"}, # Eye of the tiger
    
    {"time": 169.132, "key": "R"},
    {"time": 169.132, "key": "Y"},

    {"time": 170.095, "key": "B"},
    {"time": 170.095, "key": "G"},

    {"time": 170.914, "key": "P"},
    {"time": 170.914, "key": "R"},
    {"time": 171.381, "key": "Y"},

    {"time": 173.525, "key": "G"},

    {"time": 174.103, "key": "B"},
    {"time": 174.103, "key": "Y"},

    {"time": 175.842, "key": "R"},

    {"time": 177.962, "key": "P"},
    {"time": 177.962, "key": "G"},

    {"time": 178.958, "key": "Y"},

    {"time": 180.161, "key": "B"},
    {"time": 180.161, "key": "P"},

    {"time": 180.699, "key": "G"},

    {"time": 181.272, "key": "R"},
    {"time": 181.272, "key": "Y"},

    {"time": 181.690, "key": "B"},
    {"time": 182.027, "key": "P"},
    {"time": 182.313, "key": "R"},

    {"time": 183.107, "key": "Y"},
    {"time": 183.107, "key": "G"},

    {"time": 184.930, "key": "B"},

    {"time": 185.114, "key": "P"},
    {"time": 185.487, "key": "R"},

    {"time": 187.409, "key": "Y"},
    {"time": 187.409, "key": "G"},

    {"time": 187.877, "key": "B"},
    {"time": 188.435, "key": "P"},

    {"time": 189.095, "key": "R"},
    {"time": 189.095, "key": "Y"},
    {"time": 189.580, "key": "B"},

    {"time": 190.135, "key": "G"},

    {"time": 190.724, "key": "P"},
    {"time": 190.724, "key": "R"},


    {"time": 191.437, "key": "R"},
    {"time": 191.437, "key": "B"},
    {"time": 192.557, "key": "Y"},
    {"time": 192.929, "key": "B"},
    {"time": 193.338, "key": "P"},
    {"time": 193.338, "key": "Y"},
    {"time": 194.742, "key": "R"},
    {"time": 195.132, "key": "Y"},
    {"time": 195.568, "key": "B"},
    {"time": 195.568, "key": "Y"},
    {"time": 196.946, "key": "P"},
    {"time": 197.335, "key": "R"},
    {"time": 197.834, "key": "Y"},
    {"time": 197.834, "key": "P"},

    {"time": 200.478, "key": "B"},
    {"time": 200.478, "key": "R"},
    {"time": 201.408, "key": "P"},
    {"time": 201.763, "key": "R"},
    {"time": 202.166, "key": "Y"},
    {"time": 202.166, "key": "B"},
    {"time": 203.580, "key": "B"},
    {"time": 203.972, "key": "P"},
    {"time": 204.400, "key": "Y"},
    {"time": 204.400, "key": "P"},
    {"time": 205.765, "key": "Y"},
    {"time": 206.155, "key": "B"},
    {"time": 206.525, "key": "B"},
    {"time": 206.525, "key": "Y"},

    {"time": 208.944, "key": "R"},
    {"time": 208.944, "key": "B"},
    {"time": 210.163, "key": "Y"},
    {"time": 210.551, "key": "B"},
    {"time": 210.991, "key": "P"},
    {"time": 210.991, "key": "Y"},
    {"time": 212.292, "key": "R"},
    {"time": 212.712, "key": "Y"},
    {"time": 213.154, "key": "B"},
    {"time": 213.154, "key": "Y"},
    {"time": 214.904, "key": "R"},
    {"time": 215.361, "key": "Y"},
    {"time": 217.855, "key": "B"},
    {"time": 217.855, "key": "Y"},

    {"time": 219.020, "key": "R"},
    {"time": 219.020, "key": "B"},
    {"time": 219.392, "key": "R"},
    {"time": 219.815, "key": "Y"},
    {"time": 221.148, "key": "P"},
    {"time": 221.148, "key": "Y"},
    {"time": 221.572, "key": "P"},
    {"time": 222.014, "key": "R"},
    {"time": 223.380, "key": "Y"},
    {"time": 223.380, "key": "B"},
    {"time": 223.754, "key": "B"},
    {"time": 224.196, "key": "P"},
    {"time": 226.623, "key": "Y"},
    {"time": 226.623, "key": "P"},
    {"time": 227.739, "key": "R"},
    {"time": 227.739, "key": "B"},
    {"time": 228.145, "key": "P"},
    {"time": 228.145, "key": "Y"},
    {"time": 228.600, "key": "P"},
    {"time": 229.937, "key": "R"},
    {"time": 230.360, "key": "Y"},
    {"time": 230.360, "key": "B"},
    {"time": 230.796, "key": "B"},
    {"time": 232.152, "key": "P"},
    {"time": 232.574, "key": "R"},
    {"time": 233.044, "key": "Y"},
]

game.load_notes(note_chart)

# --- Game states ---
STATE_START = "start_screen"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "end_screen"
game_state = STATE_START
hit_feedback = ""
feedback_timer = 0
feedback_y_offset = 0

# --- Draw start screen ---
def draw_start_screen():
    screen.fill((20, 20, 20))
    title = title_font.render("Guitar Hero", True, WHITE)
    song = big_font.render("Eye of the Tiger", True, WHITE)
    info = font.render("Press ENTER to Start", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(song, (SCREEN_WIDTH//2 - song.get_width()//2, SCREEN_HEIGHT//2 - 20))
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2 + 60))
    pygame.display.flip()

# --- Draw hollow hit zones with glow ---
def draw_hit_zone():
    for lane_index, x in LANE_X.items():
        # Glow circle
        pygame.draw.circle(screen, (*LANE_COLORS[lane_index], 80), (x, HIT_Y), NOTE_RADIUS+12, 6)
        # Hollow circle
        pygame.draw.circle(screen, LANE_COLORS[lane_index], (x, HIT_Y), NOTE_RADIUS, 4)

# --- Draw end screen ---
def draw_end_screen():
    screen.fill((20, 20, 20))
    title = title_font.render("Song Complete!", True, WHITE)
    score_text = big_font.render(f"Score: {game.score}", True, WHITE)
    combo_text = font.render(f"Max Combo: {game.max_combo}", True, WHITE)
    hits_text = font.render(f"Total Hits: {game.total_hits}", True, WHITE)
    misses_text = font.render(f"Total Misses: {game.total_misses}", True, WHITE)
    restart_text = font.render("Press ENTER to Restart", True, WHITE)

    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 180))
    screen.blit(combo_text, (SCREEN_WIDTH//2 - combo_text.get_width()//2, 260))
    screen.blit(hits_text, (SCREEN_WIDTH//2 - hits_text.get_width()//2, 320))
    screen.blit(misses_text, (SCREEN_WIDTH//2 - misses_text.get_width()//2, 360))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 440))
    pygame.display.flip()

# --- Animate feedback ---
def draw_feedback():
    global feedback_y_offset
    if feedback_timer > 0:
        feedback_surface = big_font.render(hit_feedback, True, WHITE)
        y_pos = HIT_Y - 60 - feedback_y_offset
        screen.blit(feedback_surface, (SCREEN_WIDTH//2 - feedback_surface.get_width()//2, y_pos))
        feedback_y_offset += 60 * (1/FPS)  # float upward

# --- Main loop ---
running = True
while running:
    delta_time = clock.tick(FPS) / 1.0

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- START SCREEN --------
        elif event.type == pygame.KEYDOWN and game_state == STATE_START:
            if event.key == pygame.K_RETURN:
                game.start()
                game_state = STATE_PLAYING
                pygame.mixer.music.play()
                song_start_time = time.time()
                beat_recording = True
                beat_times = []
                print("\nBeat Recording Started!\nPress SPACE on every note.\n")

        # -------- KEYBOARD INPUT --------
        elif event.type == pygame.KEYDOWN and game_state == STATE_PLAYING:

            # FRET KEYS
            if event.key == pygame.K_d: current_fret = "d"
            elif event.key == pygame.K_f: current_fret = "f"
            elif event.key == pygame.K_j: current_fret = "j"
            elif event.key == pygame.K_k: current_fret = "k"
            elif event.key == pygame.K_l: current_fret = "l"

            # STRUM
            elif event.key == pygame.K_a:
                strum_triggered = True

            # Pause toggle
            elif event.key == pygame.K_p:
                game.toggle_pause()

    # ==================================================
    # 1. ARDUINO INPUT (OUTSIDE EVENT LOOP — ALWAYS RUNS)
    # ==================================================
    if arduino_input:
        print("RECEIVED:", arduino_input)

        # ---------- FRET DOWN ----------
        if arduino_input.endswith("_DOWN"):
            fret = arduino_input[0]   # get 'd','f','j','k','l'
            if fret in fret_down:
                fret_down[fret] = True

        # ---------- FRET UP ----------
        elif arduino_input.endswith("_UP"):
            fret = arduino_input[0]
            if fret in fret_down:
                fret_down[fret] = False

        # ---------- STRUM ----------
        elif arduino_input in ["STRUM_DOWN", "STRUM_UP"]:
            strum_triggered = True

        arduino_input = None  # clear
    
    # ==================================================
    # UPDATE CURRENT_FRET BASED ON HELD FRETS
    # ==================================================

#THIS UPDATES LASTLY
    # Only override current_fret if a fret is being held on Arduino
    held = [f for f in fret_down if fret_down[f]]

    if held:
        current_fret = held[0]   # pick the first held fret
    # else: do NOT reset current_fret — preserve keyboard input


    

    # ==================================================
    # 2. UNIVERSAL HIT CHECK (WORKS FOR BOTH INPUT TYPES)
    # ==================================================
    if strum_triggered and current_fret:
        result = game.handle_input(current_fret)
        print("ATTEMPT HIT:", current_fret)
        strum_triggered = False

        if result:
            hit_feedback = result
            feedback_timer = 0.5
            feedback_y_offset = 0

    # --- Update game logic ---
    if game_state == STATE_PLAYING:
        game.update()

    # --- End song after 4:02 ---
    if game_state == STATE_PLAYING and song_start_time:
        if time.time() - song_start_time >= SONG_LENGTH:
            pygame.mixer.music.stop()
            game_state = STATE_GAME_OVER

    # --- Draw everything ---
    screen.fill((20, 20, 20))

    if game_state == STATE_START:
        draw_start_screen()
    elif game_state == STATE_PLAYING:
        draw_hit_zone()
        game.draw(screen)
        draw_feedback()

        score_text = font.render(f"Score: {game.score}", True, WHITE)
        combo_text = font.render(f"Combo: {game.combo}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 50))

    elif game_state == STATE_GAME_OVER:
        draw_end_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
