class Page():

    def __init__(self, config, flags, combiner, inventory):
        import pygame
        from os import chdir
        from os.path import dirname
        import sys
        import os        
        from modules.glyph import Glyph, Macros
      
        self.clock = pygame.time.Clock()
        self.config = config
        self.folder = config.RESOURCES
        self.screen = config.SCREEN
        self.size = config.SCREEN_SIZE
        self.defaults = config.DEFAULT
        self.background = config.BKGSCREEN
        self.inventory = inventory
        self.combiner = combiner
        self.flags = flags       
        
        self.glyph_rect = pygame.Rect(0, 0, 560, 270)
        self.old_rect = self.glyph_rect
        self.find_position(self.background, self.glyph_rect)       
        self.glyph = Glyph(self.glyph_rect, **self.defaults) 
        self.offset = self.glyph.rect.topleft        
        self.glyph.image.set_alpha(255)
        self.clear = self.glyph.image.copy()
        self.clear.fill((0,0,0))
        # self.mask = pygame.mask.from_surface(self.glyph.image)
        
        self.fade = []
        self.fade_type = "word"
        self.fade_rate = 10
        self.tick = 0

       
        Macros["default"] = ("color", (200, 200, 200)) 
        

    def find_position(self, surface, rect):
        surfrect = surface.get_rect()
        rect.x = ((surfrect.w / 2) - (rect.w / 2))
        rect.y = ((surfrect.h / 2) - (rect.h / 2)) - 70 
            
    def update(self, input, links, raw):    
        self.glyph.clear(self.screen, self.background)
        self.glyph.input(input, justify = "justified")
        self.glyph.update()
        self.populate(links)
        self.fade = []
        self.final = []
        self.find_tokens(raw)
               

    def populate(self, links):        
        from page import Hyperlink
        self.hyperlinks = []
        for link in links:
            rect = self.find_rect(link[2])
            hyperlink = Hyperlink(link, rect, self.defaults, self.screen, self.glyph_rect, self.flags, self.combiner, self.inventory, self.config)
            self.hyperlinks.append(hyperlink)

    def find_tokens(self, raw):
        import pygame

        links = self.glyph.links
        wordglyph = self.glyph.tokens
        # print wordglyph
    
        link_random = []
        for link in links.items():
            for rect in link[1]:
                link_random.append(rect)         
        
        link_lines = {}
        for rect in link_random:
            y = rect[1]
            if link_lines.has_key(y):
                link_lines[y].append(rect)
            else:
                link_lines[y] = [rect]
        
        link_list = link_lines.items()
        link_list.sort()

        wordcount = 0
        thislist = []

        for line in link_list:

            rectlist = line[1]
            length = len(rectlist)      
            rectlist.sort()
            rectcount = 0

            for rect in rectlist:
                if rectcount == 0:
                    if wordglyph[wordcount] == " ":
                        wordcount += 1
                if rectcount == length-1:
                    
                    if wordglyph[wordcount] == " ":
                        wordcount += 1
                if wordglyph[wordcount] == '\n':
                    item = " "
                else:
                    item = wordglyph[wordcount]
                tpl = (item, rect)
                thislist.append(tpl)
                wordcount += 1
                rectcount += 1     

        link_order = []
      
        for line in link_list:
            rects = line
            line[1].sort()
            link_order.extend(line[1])
        
        for item in link_order:           
            item.move_ip(self.offset)

        self.fade_word = thislist 

        charlist =  []
        color = (0,0,0)
        font = self.config.FONT
        for tpl in self.fade_word:
            txt = tpl[0]
            rect = tpl[1]
            if len(txt) == 1:
                charlist.append(tpl)
            else:
                coords = rect[0], rect[1]
                for char in txt:
                    char_text = font.render(char,0,color)
                    char_rect = char_text.get_rect()
                    char_rect.move_ip(coords)

                    width = char_text.get_width()
                    coords = char_rect[0]+width, char_rect[1]
                    char_tpl = char, char_rect
                    charlist.append(char_tpl)
        self.fade_char = charlist

        if self.fade_type == "char":
            self.fade_order = self.fade_char
        elif self.fade_type == "word":
            self.fade_order = self.fade_word


    def draw(self, tick):
        import pygame
        font = self.config.FONT
        # color = (135, 135, 200)
        color = (200,200,200)
        self.fade_in(tick)
        self.draw_links() 
        
        if len(self.fade_word) <> len(self.fade):
            self.screen.blit(self.clear, self.glyph_rect)          
            for item in self.fade:
                text = font.render(item[0], 0, color)
                rect = item[1]
                self.screen.blit(text, rect)
            

    def fade_in(self, tick):
        self.tick += tick        
        speed = self.fade_rate

        if self.fade_type == "char":
            if self.tick > speed:
                length = len(self.fade)
                if length < len(self.fade_order):
                    self.fade.append(self.fade_order[length])
                    self.tick = 0
        if self.fade_type == "word":
            if self.tick > speed:
                length = len(self.fade)
                if length < len(self.fade_order):
                    self.fade.append(self.fade_order[length])
                    self.tick = 0


   
    def find_rect(self, link):
        # print link
        rect = None
        for item in self.glyph.links.items():            
            if item[0] == link:
                rect = item[1][0]
                return rect    
                      # sem pride koda za return rects
        
    def draw_links(self):
        import pygame
        mpos = pygame.mouse.get_pos() 
        self.get_collisions(mpos)          
        

        self.screen.blit(self.glyph.image, self.glyph_rect)         
        for link in self.hyperlinks:
            link.draw()
       

    def get_collisions(self, mpos):
        import pygame
        mrect = pygame.Rect(mpos, (1,1))
        for hyperlink in self.hyperlinks:
            hyperlink.determine_distance(mrect)
            if mrect.colliderect(hyperlink.rect):                                
                hyperlink.hover = True               
            else:
                hyperlink.hover = False    

    def find_hover(self):
        for hyperlink in self.hyperlinks:                       
            if hyperlink.hover == True:
                return hyperlink.content
            else:
                return None     


class Hyperlink():
    def __init__(self, link, rect, defaults, screen, glyph_rect, flags, combiner, inventory, config): 
        self.combiner = combiner
        self.flags = flags
        self.inventory = inventory     
        self.word = link[0]
        self.content = link[1]
        self.config = config
        self.rect = rect
        self.color_hidden = self.config.DEFAULT["color"]
        self.color_hover = (255,255,255)
        self.color_default = (135, 13, 145)
        self.defaults = defaults
        self.screen = screen
        self.font = self.defaults["font"]
        self.get_position(glyph_rect)
        self.hover = False
        self.distance = 0
        self.visible = self.determine_visibility()    
        

    def get_position(self, glyph_rect):
        x = glyph_rect[0]
        y = glyph_rect[1]
        self.rect = self.rect.move(x,y)

    
    def draw(self): 
        import pygame 
        color = self.determine_color() 
        text = self.font.render(self.word, 2, color)
        rect = self.rect  

        blank = pygame.Surface((rect[2],rect[3]))
        blank.convert()
        blank.fill((0,0,0))     
                
        self.screen.blit(blank, rect)
        self.screen.blit(text, rect)

    def determine_color(self):
        color_text = (200, 200, 200)
        color_active = (135, 13, 145)
        color_selected = (255, 255, 255)
        if self.hover is True:
            color = color_selected      
        else:
            color = color_active

        if self.visible == False:
            color = color_text

        if self.check_clue() == True:            
            color = self.mix_color()        

        return color

    def determine_visibility(self):  
        
        if self.flags.check(self.content, "=", 1): 
            # pygame.mouse.set_cursor(*HAND_CURSOR)             
            return True
        else:             
            return False
            # pygame.mouse.set_cursor(*DEFAULT_CURSOR)  

    def determine_distance(self, mpos):
        import math
        center = self.rect.center
        link_x = center[0]
        link_y = center[1]
        mouse_x = mpos[0]
        mouse_y = mpos[1]
        distance = math.sqrt((link_x-mouse_x)**2 + (link_y-mouse_y)**2)
        distance = math.trunc(distance)
        self.distance = distance

    def check_clue(self):
        from tools import check_flags
        if len(self.combiner.box) == 1:            
            item_id = self.combiner.box[0] 
            if self.visible == False:           
                link_id = self.content
                for entity in self.inventory.pool:
                    if entity.id == item_id:
                        item = entity
                        for revealed_link in item.reveal:
                            if revealed_link[0] == link_id:
                                if check_flags(revealed_link, self.flags):
                                    return True
        else:
            return False   

    def mix_color(self): 
        if self.distance <= 55:       
            distance = 55 - self.distance
        else:
            distance = 0
        hue = 200 + distance
        color = (hue,hue,hue)        
        return color             
 