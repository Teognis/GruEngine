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
SCREEN_SIZE = (1000, 640)
SCREEN = display.set_mode(SCREEN_SIZE)

# image constants
BKGSCREEN = pygame.Surface(SCREEN_SIZE)
BKGSCREEN = BKGSCREEN.convert()

#glyph constants
FONT = Font(os.path.join(RESOURCES, "font", "advert.ttf"), 14)
DEFAULT = {
    'bkg'       : (0,0,0),
    'color'     : (201, 192, 187),
    'font'      : FONT,
    'spacing'   : 2, 
}

color_text = (201, 192, 187)
color_active = (135, 13, 145)
color_selected = (255, 255, 255)


#functions
def center(surf, rect):
# centers rectangles on a specified axis on a surface
    surfrect = surf.get_rect()
    rect.x = ((surfrect.w / 2) - (rect.w / 2))
    rect.y = ((surfrect.h / 2) - (rect.h / 2))
            
#prepare rects and surfaces
CLIP = Rect(0, 0, 560, 320)
center(BKGSCREEN, CLIP)
COMPRECT = Rect(412,530,150,150)

BKGSCREEN.set_clip(None) #prej clip
BKGSCREEN.fill((0,0,0))

CLIP.w -= 10
CLIP.h -= 10
center(BKGSCREEN, CLIP)

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
combiner = Combiner(COMBINATIONS, flags)
state = State(SCENES, LINKS, flags, inventory, wheel, combiner, title)
menu = Menu(SCREEN, SCREEN_SIZE, RESOURCES, SAVE, state)
menu.new_game()
pagetext = state.output

class Main():

#   Example usage of Glyph

    def __init__(self):
        self.glyph = Glyph(CLIP, **DEFAULT)      
          
    def start(self):
        """

        """
        SCREEN.blit(BKGSCREEN, (0, 0))      
       
        
        def find_macros(text, Macros):
            macros = []            
            text = text.split()
            for word in text:
                if word.startswith("lnk_"):
                    word = word.rstrip(";")
                    macros.append(word)
            for link in macros:
                if flags.check(link, "=", 1):
                    color = color_active
                else:
                    color = color_text            
                Macros[link] = ("color", color)           
   
        
        def glyph_draw(input, link, flags):
            glyph.clear(SCREEN, BKGSCREEN)
            find_macros(input, Macros)
            if link is not None:                
                if flags.check(link, "=", 1):
                    color = color_selected
                else:
                    color = color_text          
                Macros[link] = ("color", color)          
            glyph.input(input, justify = 'justified')
            glyph.update()
               

        glyph = self.glyph
        glyph_rect = glyph.rect
        glyph.image.set_alpha(255)        
        glyph_draw(state.output, None, flags) 
                     
        while 1:            
            mpos = mouse.get_pos()
            mrect = Rect(mpos, (1,1))  
            lnk_click = glyph.get_collisions(mouse.get_pos())
            menu_click = menu.get_collisions(mrect)               
            whl_click = wheel.get_collisions(mrect)  
            inv_click = inventory.get_collisions(mrect)
                            
            if lnk_click:              
                glyph_draw(state.output, lnk_click, flags)   
                if flags.check(lnk_click, "=", 1): mouse.set_cursor(*HAND_CURSOR)                                
            else:             
                glyph_draw(state.output, None, flags)
                mouse.set_cursor(*DEFAULT_CURSOR)

            SCREEN.blit(glyph.image, glyph_rect) 
            menu.draw()           
            state.draw()
            state.inventory.get_collisions(mrect)

            if inv_click[0] is not None: state.inventory.draw_selection(*inv_click)
            if menu_click is not None: menu.draw_selection(menu_click)

            for ev in event.get():

                if ev.type == MOUSEBUTTONDOWN:
                    if ev.button == 1:
                        if menu_click is 0: menu.new_game()
                        elif menu_click is 3: exit()
                        menu.set_focus(menu_click)
                        state.input(lnk_click, whl_click, inv_click,"left", "down")                        

                if ev.type == MOUSEBUTTONUP:
                    if ev.button == 1:
                        state.input(lnk_click, whl_click, inv_click,"left", "up")
                    if ev.button == 3: 
                        state.input(lnk_click, whl_click, inv_click,"right", "up")
                                     
                if ev.type == KEYDOWN: 

                    if ev.key == K_ESCAPE: 
                        if menu.focus == None: 
                            exit() 
                        else:
                            menu.input(ev.key)
                        
                    else:                                            
                        menu.input(ev.key)              

            display.update()

if __name__ == '__main__':
    main = Main()
    main.start()
