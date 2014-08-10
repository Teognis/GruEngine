__author__ = 'Teognis'
import pygame
import os
from os import chdir
from os.path import dirname
import random
import time
import yaml
import sys

RESOURCES = os.path.join(dirname(__file__), "resources",)
DATA = os.path.join(dirname(__file__), "data",)
SYSTEM = os.path.join(dirname(__file__), "system")
SAVE = os.path.join(dirname(__file__), "save")
sys.path.insert(0, SYSTEM)

from flags import Flags, Flag
from state import State
from scene import Scene, Line, Link, Title
from wheel import Wheel, Wlink, Anchor
from inventory import Inventory
from combiner import Combiner, Combination 
from tools import glyph_links
from menu import Menu
from collider import Collider
from page import Page
from glyph import Editor, Glyph, Macros, Text
from pygame import display
from pygame import event
from pygame.font import Font
from pygame import image
from pygame import mouse
from pygame import transform
from pygame.locals import *

pygame.init()

# screen constants
SCREEN_SIZE = (1000, 800)
# SCREEN = display.set_mode(SCREEN_SIZE)
SCREEN = display.set_mode(SCREEN_SIZE)

# image constants
BKGSCREEN = pygame.Surface(SCREEN_SIZE)
BKGSCREEN = BKGSCREEN.convert()

#glyph constants
FONT = Font(os.path.join(RESOURCES, "font", "advert.ttf"), 15)
DEFAULT = {
    'bkg'       : (0,0,0),
    'color'     : (200, 200, 200),
    'font'      : FONT,
    'spacing'   : 2, 
}

# prepare cursors
#the default cursor
DEFAULT_CURSOR = mouse.get_cursor()

#the hand cursor
_HAND_CURSOR = (
    "     XX         ",
    "    X..X        ",
    "    X..X        ",
    "    X..X        ",
    "    X..XXXXX    ",
    "    X..X..X.XX  ",
    " XX X..X..X.X.X ",
    "X..XX.........X ",
    "X...X.........X ",
    " X.....X.X.X..X ",
    "  X....X.X.X..X ",
    "  X....X.X.X.X  ",
    "   X...X.X.X.X  ",
    "    X.......X   ",
    "     X....X.X   ",
    "     XXXXX XX   ")
_HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)

scenestream = file(os.path.join(DATA, "scenes.yml"), "r")
SCENES = yaml.load(scenestream)
scenestream.close()
linkstream = file(os.path.join(DATA, "links.yml"), "r")
LINKS = yaml.load(linkstream)
linkstream.close()
flagstream = file(os.path.join(DATA, "flags.yml"), "r")
FLAGS = yaml.load(flagstream)
flagstream.close()
itemstream = file(os.path.join(DATA, "items.yml"), "r")
ITEMS = yaml.load(itemstream)
itemstream.close()
cluestream = file(os.path.join(DATA, "clues.yml"), "r")
CLUES = yaml.load(cluestream)
cluestream.close()
combinationstream = file(os.path.join(DATA, "combinations.yml"), "r")
COMBINATIONS = yaml.load(combinationstream)
combinationstream.close()

flags = Flags(FLAGS)
wheel = Wheel(SCREEN, SCREEN_SIZE, RESOURCES)
title = Title(SCREEN, SCREEN_SIZE, RESOURCES)
inventory = Inventory(ITEMS, CLUES, flags, SCREEN, SCREEN_SIZE, RESOURCES)
combiner = Combiner(COMBINATIONS, flags, inventory)
page = Page(DEFAULT, SCREEN, BKGSCREEN, flags)
state = State(SCENES, LINKS, flags, inventory, wheel, combiner, title, page)
menu = Menu(SCREEN, SCREEN_SIZE, RESOURCES, SAVE, state)
collider = Collider(page,menu,wheel,inventory)
# menu.new_game()


class Main():

#   Example usage of Glyph

    def __init__(self):
        menu.new_game()
                               
    def start(self):
        """

        """        
        
        clock = pygame.time.Clock()        
                     
        while 1:                
            clock.tick()
            # print clock.get_fps()                     
            mpos = mouse.get_pos()
            mrect = Rect(mpos, (1,1))              
            menu.draw()           
            state.draw()
            state.inventory.get_collisions(mrect)

            for ev in event.get():

                if ev.type == MOUSEBUTTONDOWN:
                    if ev.button == 1:                      
                        menu.input(collider.get(), "left", "down")
                    if ev.button == 3:
                        menu.input(collider.get(),"right", "up")           

                if ev.type == MOUSEBUTTONUP:
                    if ev.button == 1:
                        menu.input(collider.get(),"left", "up")
                    if ev.button == 3: 
                        menu.input(collider.get(),"right", "up")
                                     
                if ev.type == KEYDOWN: 
                    if ev.key == K_ESCAPE: 
                        if menu.focus == None: 
                            exit() 
                        else:
                            menu.enter(ev.key)                        
                    else:                                            
                        menu.enter(ev.key)  


            display.update()

if __name__ == '__main__':
    main = Main()
    main.start()
