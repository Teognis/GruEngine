# -*- coding: cp1250 -*-
__author__ = 'Teognis'
import pygame
import os

from os import chdir
from os.path import dirname
import random
import time
import yaml
#import wheel

#from Text import PAGES, WHEEL, DYNAMIC, STATIC, OVERRIDE, WUPDATE, REPLACE

from wheel import Wheel
from glyph import Editor, Glyph, Macros, Text
from pygame import display
from pygame import event
from pygame.font import Font
from pygame import image
from pygame import mouse
from pygame import transform
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2)
pygame.init()

# path constants
DIRNAME = os.path.join(dirname(__file__), "resources",)

# screen constants
SCREEN_SIZE = (1000, 640)
SCREEN = display.set_mode(SCREEN_SIZE)

# image constants
BKGSCREEN = image.load(os.path.join(DIRNAME, "img", "bkgscreen.tga"))
BKGSCREEN = transform.scale(BKGSCREEN, SCREEN_SIZE)
BKGSCREEN = BKGSCREEN.convert()
WORD = image.load(os.path.join(DIRNAME, "img", "word.png"))
TRIANGLE = image.load(os.path.join(DIRNAME, "img", "ptriangle.png"))
TRIANGLEN = transform.smoothscale(TRIANGLE, (25,25))
TRIANGLENW = transform.rotate(TRIANGLEN, 45)
TRIANGLEW = transform.rotate(TRIANGLEN,90)
TRIANGLESW = transform.rotate(TRIANGLEN, 135)
TRIANGLES = transform.rotate(TRIANGLEN,180)
TRIANGLESE = transform.rotate(TRIANGLEN,225)
TRIANGLEE = transform.rotate(TRIANGLEN,270)
TRIANGLENE = transform.rotate(TRIANGLEN,315)

#glyph constants
FONT = Font(os.path.join(DIRNAME, "font", "advert.ttf"), 14)
DEFAULT = {
    'bkg'       : (0,0,0),
    'color'     : (201, 192, 187),
    'font'      : FONT,
    'spacing'   : 2, #FONT.get_linesize(),
}

#functions
def center(surf, rect):
# centers rectangles on a specified axis on a surface
    surfrect = surf.get_rect()
    rect.x = ((surfrect.w / 2) - (rect.w / 2))
    rect.y = ((surfrect.h / 2) - (rect.h / 2))


def update_macro(list, word):               #updates the color dictionary for Glyph links (each link gets its own colour - prohack.com)
    list[word] = ("color", (135,13,145))


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


#prepare the pages of text
PAGES = {"Field" : "This is <right>"}
STATUS = {'current' : 'test', 'state' : 'Field'};
FLAGS = {}

scenestream = file("scenes.yml", "r")
SCENES = yaml.load(scenestream)


wheel = Wheel(SCREEN_SIZE)


def glyph_links(text):              #creates Glyph markup out of Grue markup :)
    linklist = []
    tuples = []
    
    splittext = text.split(">")                 
    for i in splittext:
        indeks = i.find("<")
        if indeks is not -1:
            length = len(i)
            word = i[indeks+1:length]                    
            if word not in linklist:                     
                linklist.append(word)
    for i in linklist:
        tpl = i.split("/")
        tuples.append(tpl)
    
    for i in tuples:
        word = i[0]
        link = i[1]
        update_macro(Macros,link)
        original = word + "/" + link
        oldstring = "<" + original + ">"
        newstring = "{link "+link+"; {"+link+"; "+word+"}}"          
        text = text.replace(oldstring, newstring)
           
    return text

   
class Line():
    def __init__(self, data):
        self.data = data
        self.req = []
        self.eff = []
        self.set_attributes(self.data)
        self.checkout = self.check_req()
        self.print_req()
        
        
    def set_attributes(self, dict):
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_pool(self):
        pass

    def interpret(self, text):
        operators = ["=+","=-",">=","<=","="]
        
        for operator in operators:
            if operator in text:
                print operator
                splittext = text.split(operator)
                
            else:
                splittext = text
        return splittext
     


    def print_req(self):
        print self.checkout

    def check_flags(self, list, flags):
        key = list[0]
        value = list[1]
        if flags.has_key(key):
            if flags[key] == value:
                return 1
        else:
            return 0        
      
    
    def check_req(self):
        reqs = self.req
        flags = {"house":3,"field":2}
        if reqs == []:
            return 1
        else:
            for req in reqs:
                newreq = self.interpret(req)
                value = self.check_flags(newreq,flags)
                if value == 0:
                    return 0
                else:
                    pass
            return 1

                                  
            
        

class Scene():

    def __init__(self, dict):      
        self.set_attributes(dict)
        self.segments = []
        self.variations = []
        self.collect_segments()
        self.collect_variations()

        
    def set_attributes(self, dict):         #pulls data out of the items.yml stream and configures the attributes of the Ability instance
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_segments(self):
        segments = []
        
        for i in self.output:
            segments.append(i)
            
        self.segments = segments
        
    def collect_variations(self):        
        segments = self.segments
        segpool = []
        for segment in segments:
            varpool = []
            for variation in segment:
                var = Line(variation)
                varpool.append(var)
            segpool.append(varpool)
        self.pool = segpool

    def create_output(self):
        output = ""
        pool = self.pool
        for segment in pool:
            for variation in segment:
                output = output + variation.txt
        output = glyph_links(output)
        
        self.output = output


field = SCENES["field"]

field = Scene(field)
##for i in field.pool:
##    for y in i:
##        y.interpret(y.eff)
field.create_output()

print field.output


pagetext = field.output



class Main():

#   Example usage of Glyph

    def __init__(self):
        self.glyph = Glyph(CLIP, **DEFAULT)


        Macros['b'] = ('font', Font(os.path.join(DIRNAME, "font", "silkscreen_bold.ttf"), 8))
        Macros['big'] = ('font', Font(os.path.join(DIRNAME, "font", "silkscreen.ttf"), 16))
        Macros['BIG'] = ('font', Font(os.path.join(DIRNAME, "font", "silkscreen_bold.ttf"), 16))
        Macros['red'] = ('color', (255, 0, 0))
        Macros['white'] = ('color', (255,255,255))
        Macros['testwhite'] = ('color', (255,0,0))
        Macros['green'] = ('color', (0, 255, 0))
        Macros['bkg_blu'] = ('bkg', (0, 0, 255))
        Macros['test'] = ('color', (135,13,145))
     
  

    def start(self):
        """

        """
        
               
        chdir(DIRNAME)
        glyph = self.glyph
        glyph_rect = glyph.rect
        glyph.image.set_alpha(255)
        SCREEN.blit(BKGSCREEN, (0, 0))
              
        while 1:                    
                                 
            mpos = mouse.get_pos()
            link = glyph.get_collisions(mouse.get_pos())           
            mrect = Rect(mpos, (1,1))            
            wlink = wheel.get_collisions(mrect)                   
                            
            if link:               
                Macros[link] = ('color', (255,255,255))
                glyph.clear(SCREEN, BKGSCREEN)
                glyph.input(pagetext, justify = 'justified')
                glyph.update()
                mouse.set_cursor(*HAND_CURSOR)

            else:
                for i in Macros:
                    Macros[i] = ('color', (135,13,145))
                glyph.clear(SCREEN, BKGSCREEN)
                glyph.input(pagetext, justify = 'justified')
                glyph.update()
                mouse.set_cursor(*DEFAULT_CURSOR)

            SCREEN.blit(glyph.image, glyph_rect)
            wheel.draw(SCREEN)

            for ev in event.get():

                if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                    if link:
                        print link
                      

                    if wlink:                        
                        wheel.input(wlink)
                        print wheel.state
                    else:
                        pass

                if ev.type == MOUSEBUTTONDOWN and ev.button == 3:                 
                                        
                    pass
                                                        
                if ev.type == KEYDOWN: exit()               

            display.update()

if __name__ == '__main__':
    main = Main()
    main.start()
