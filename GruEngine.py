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
COMPILER = os.path.join(dirname(__file__), "compile")
LIBRARY = os.path.join(dirname(__file__), "library")
gru_file = LIBRARY + "\Power.gru"
sys.path.insert(0, SYSTEM)
sys.path.insert(0, COMPILER)

from flags import Flags, Flag
from state import State
from scene import Scene, Line, Link, Title
from wheel import Wheel, Wlink, Anchor
from inventory import Inventory
from combiner import Combiner, Combination 
from tools import glyph_links
from menu import Menu
from collider import Collider
from compiler import Compiler
from page import Page
from glyph import  Glyph
from pygame import display, event, image, mouse, transform
from pygame.font import Font
from pygame.locals import *

pygame.init()

# screen constants
SCREEN_SIZE = (1000, 800)
SCREEN = display.set_mode(SCREEN_SIZE)

# SCREEN_SIZE = (1650, 1050)
# SCREEN = display.set_mode(SCREEN_SIZE, FULLSCREEN)

# image constants
BKGSCREEN = pygame.Surface(SCREEN_SIZE)
BKGSCREEN = BKGSCREEN.convert()

#glyph constants
FONT = Font(os.path.join(RESOURCES, "font", "advert.ttf"), 16)
DEFAULT = {
    'bkg'       : (0,0,0),
    'color'     : (200, 200, 200),
    'font'      : FONT,
    'spacing'   : 2, 
}



class Main():

    def __init__(self, file=None):  
        self.compiler = Compiler(file)
        self.stream = self.compiler.stream
        self.canvas_data = [SCREEN, SCREEN_SIZE, RESOURCES]
        self.flags = Flags(self.stream)
        self.wheel = Wheel(*self.canvas_data)
        self.title = Title(*self.canvas_data)
        self.inventory = Inventory(self.stream, self.flags, *self.canvas_data)
        self.combiner = Combiner(self.stream, self.flags, self.inventory)
        self.page = Page(DEFAULT, SCREEN, BKGSCREEN, self.flags, self.combiner, self.inventory)
        self.state = State(self.stream, self.flags, self.inventory, self.wheel, self.combiner, self.title, self.page)
        self.menu = Menu(SCREEN, SCREEN_SIZE, RESOURCES, SAVE, self.state)
        self.collider = Collider(self.page,self.menu,self.wheel,self.inventory,self.flags)
        self.menu.new_game() 

    def draw(self):
        self.menu.draw()   
        self.state.draw()    
                               
    def start(self):     
        
        clock = pygame.time.Clock()        
                     
        while 1:                
            clock.tick()
            # print clock.get_fps()                    
            mrect = Rect(mouse.get_pos(), (1,1))    
            self.collider.check()          
            self.draw()           

            for ev in event.get():

                if ev.type == MOUSEBUTTONDOWN:
                    if ev.button == 1:                      
                        self.menu.input(self.collider.get(), "left", "down")
                    if ev.button == 3:
                        self.menu.input(self.collider.get(), "right", "up")           

                if ev.type == MOUSEBUTTONUP:
                    if ev.button == 1:
                        self.menu.input(self.collider.get(),"left", "up")
                    if ev.button == 3: 
                        self.menu.input(self.collider.get(),"right", "up")
                                     
                if ev.type == KEYDOWN: 
                    if ev.key == K_ESCAPE: 
                        if self.menu.focus == None: 
                            exit() 
                        else:
                            self.menu.enter(ev.key)                        
                    else:                                            
                        menu.enter(ev.key)  

            display.update()

if __name__ == '__main__':
    main = Main()
    main.start()
