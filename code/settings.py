import os

path_main = os.path.abspath(__file__).replace("\\", "/")
path_main = path_main.replace("code/settings.py", "")


# game setup
WIDTH    = 640
HEIGTH   = 640
FPS      = 40
TILESIZE = 64