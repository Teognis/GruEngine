import pygame
import os
from os import chdir
from os.path import dirname
import random
import time
import yaml
import sys
from flags import Flags, Flag
from state import State
from scene import Scene, Line, Link, Title
from wheel import Wheel, Wlink, Anchor
from inventory import Inventory
from combiner import Combiner, Combination 
from tools import glyph_links
from menu import Menu
from collider import Collider
from compiler import Compiler, Stream
from page import Page
from glyph import  Glyph
from library import Library
from pygame import display, event, image, mouse, transform
import config


class Game():   
    
    def __init__(self, gru_file):
        
        self.compiler = Compiler(gru_file)
        self.stream = self.compiler.stream
        print self.stream.metadata     
        self.metadata = self.stream.metadata   
        self.flags = Flags(self.stream)
        self.wheel = Wheel(config)
        self.title = Title(config)
        self.inventory = Inventory(self.stream, self.flags, config)
        self.combiner = Combiner(self.stream, self.flags, self.inventory)
        self.page = Page(config, self.flags, self.combiner, self.inventory)
        self.state = State(self.stream, self.flags, self.inventory, self.wheel, self.combiner, self.title, self.page)               
        if self.metadata.has_key("start"):
            start = self.metadata["start"]
            self.state.update(start)
        else:
            self.state.update("start")

    def draw(self, tick):
        self.inventory.draw()
        self.wheel.draw()
        self.title.draw()
        self.page.draw(tick)

    
        
        
        