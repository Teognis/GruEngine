# -*- coding: cp1250 -*-
__author__ = 'Teognis'
import pygame
import os
from os import chdir
from os.path import dirname
import random
import time
import yaml
from title import Title
from state import State
from scene import Scene
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



FLAGS = {"graveseen" : 2, "thisguys" : 3, "thisis" : 4}

scenestream = file("scenes.yml", "r")
SCENES = yaml.load(scenestream)
scenestream.close()
wheel = Wheel(SCREEN, SCREEN_SIZE)
title = Title(SCREEN, SCREEN_SIZE)
state = State(SCENES, FLAGS, wheel, title)
state.update("field")
pagetext = state.output


class Main():

#   Example usage of Glyph

    def __init__(self):
        self.glyph = Glyph(CLIP, **DEFAULT)  
        Macros['lnk_mailbox'] = ('color', (255,255,255))    
        Macros['lnk_house'] = ('color', (255,255,255)) 
        Macros['lnk_graves'] = ('color', (255,255,255)) 
        Macros['lnk_angel'] = ('color', (255,255,255)) 
        
        
  
    def start(self):
        """

        """
        SCREEN.blit(BKGSCREEN, (0, 0))
        
        def glyph_draw(input):
            glyph.clear(SCREEN, BKGSCREEN)                
            glyph.input(input, justify = 'justified')
            glyph.update()
               
        chdir(DIRNAME)
        glyph = self.glyph
        glyph_rect = glyph.rect
        glyph.image.set_alpha(255)
        
        glyph_draw(state.output)
        wheel.draw()

               
       
              
        while 1:    
        
            mpos = mouse.get_pos()
            link = glyph.get_collisions(mouse.get_pos())           
            mrect = Rect(mpos, (1,1))            
            wclick = wheel.get_collisions(mrect)            
            
                            
            if link:               
                Macros[link] = ('color', (255,255,255))
                glyph_draw(state.output)                
                mouse.set_cursor(*HAND_CURSOR)
            else:              
                for i in Macros:
                    Macros[i] = ('color', (135,13,145))
                glyph_draw(state.output)
                mouse.set_cursor(*DEFAULT_CURSOR)
            SCREEN.blit(glyph.image, glyph_rect)
            state.draw()
            
            

            for ev in event.get():

                if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                    if link:
                        print link

                    if wclick is not None:
                        state.input(wclick, "left")                                                           
                    else:
                        pass

                if ev.type == MOUSEBUTTONDOWN and ev.button == 3: 
                    if link:
                        print link               
                    if wclick is not None:                        
                        state.input(wclick, "right")                        
                    else:
                        pass                  
                                                        
                if ev.type == KEYDOWN: exit()               

            display.update()

if __name__ == '__main__':
    main = Main()
    main.start()
