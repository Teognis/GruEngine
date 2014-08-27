import pygame
import os
from os import chdir
from os.path import dirname
import random
import time
import yaml
import sys
from pygame import display, event, image, mouse, transform
from pygame.font import Font
from pygame.locals import *

pygame.init()

RESOURCES = os.path.join(dirname(__file__), "resources",)
DATA = os.path.join(dirname(__file__), "data",)
SYSTEM = os.path.join(dirname(__file__), "system")
SAVE = os.path.join(dirname(__file__), "save")
COMPILER = os.path.join(dirname(__file__), "compile")
LIBRARY = os.path.join(dirname(__file__), "library")
sys.path.insert(0, SYSTEM)
sys.path.insert(0, COMPILER)

# screen constants
# SCREEN_SIZE = (800, 600)
# SCREEN = display.set_mode(SCREEN_SIZE)

SCREEN_SIZE = (1650, 1050)
SCREEN = display.set_mode(SCREEN_SIZE, FULLSCREEN)

# image constants
BKGSCREEN = pygame.Surface(SCREEN_SIZE)
BKGSCREEN = BKGSCREEN.convert()

#glyph constants
GLYPH_RECT = pygame.Rect(0, 0, 560, 270)
FONT = Font(os.path.join(RESOURCES, "font", "advert.ttf"), 16)
# FONT = Font(os.path.join(RESOURCES, "font", "silkscreen.ttf"), 16)
# FONT = Font(os.path.join(RESOURCES, "font", "a_AntiqueGr.ttf"), 16)

DEFAULT = {
    'bkg'       : (0,0,0),
    'color'     : (200, 200, 200),
    'font'      : FONT,
    'spacing'   : 3, 
}

CLOCK_COLOR = (200,200,200)
CLOCK_OFFSET = 10
CLOCK_SIZE = 16
CLOCK_POS =  CLOCK_OFFSET, SCREEN_SIZE[1] - CLOCK_OFFSET - CLOCK_SIZE