__author__ = 'Teognis'
import pygame
import os
from os import chdir
from os.path import dirname
import random
import time
import sys

RESOURCES = os.path.join(dirname(__file__), "resources",)
DATA = os.path.join(dirname(__file__), "data",)
SYSTEM = os.path.join(dirname(__file__), "system")
SAVE = os.path.join(dirname(__file__), "save")
COMPILER = os.path.join(dirname(__file__), "compile")
LIBRARY = os.path.join(dirname(__file__), "library")
MODULES = os.path.join(dirname(dirname(__file__)), "modules") 

sys.path.insert(0, MODULES)
sys.path.insert(0, SYSTEM)
sys.path.insert(0, COMPILER)

from menu import Menu
from collider import Collider
from library import Library
from game import Game
from dispatcher import Dispatcher
from fps import Fps

from pygame import display, event, image, mouse, transform
from pygame.locals import *
import config

class Main():

    def __init__(self, gru_file=None): 
        self.menu = Menu(self, config, game = None)        
        self.library = Library(self, config)
        self.collider = Collider(self.menu, self.library, game=None)
        self.dispatcher = Dispatcher(self.collider, self.library, self.menu, game=None)
        self.clock = pygame.time.Clock()
        self.fps = Fps(self.clock, config)
        if gru_file is not None:
            game = Game(gru_file)
            self.load(game)
        else:
            self.game = None        
        
    def load(self, game):
        self.library.clear()
        self.game = game
        self.collider.game = game
        self.menu.game = game

    def clear(self):
        self.game = None
        self.collider.game = None
        self.menu.game = None

    def draw(self):    
        tick = self.clock.get_time()
        self.menu.draw()    
        if self.game == None:
            self.library.draw()  
        else:           
            self.game.draw(tick)        

                                  
    def start(self):                          
                     
        while 1:      
            self.clock.tick()                   
            mrect = Rect(mouse.get_pos(), (1,1))  
            self.collider.check()          
            self.draw()  
            self.fps.draw()            

            for ev in event.get():
                self.dispatcher.process(ev)               

            display.update()

if __name__ == '__main__':
    main = Main()
    main.start()
