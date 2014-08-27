class Inventory():

        def __init__(self, stream, flags, config):

            self.folder = config.RESOURCES
            self.screen = config.SCREEN
            self.size = config.SCREEN_SIZE
            
            self.itm_data = stream.items
            self.clu_data = stream.clues
            self.flags = flags            
      
            self.x = self.size[0]
            self.y = self.size[1]
            self.padding = 30
            self.spacing = 10
            self.txt_color = (201, 192, 187)
            self.txt_size = 14
                        
            self.pool = []
            self.items = []            
            self.clues = []            
            self.itm_rects = []
            self.clu_rects = []
            
            self.populate()
            self.update()            
            self.find_positions()
            
            
        def populate(self):
            from inventory import Item
            from inventory import Clue
            pool = []
            for itm in self.itm_data:
                data = self.itm_data[itm]
                id = str(itm)
                item = Item(data, id, self.flags)
                pool.append(item)
            for clu in self.clu_data:
                data = self.clu_data[clu]
                id = str(clu)
                clue = Clue(data, id, self.flags)
                pool.append(clue)
            self.pool = pool

        def update(self):
            items = []
            clues = []
            # self.clear()
            for element in self.pool:
                element.update()
                if element.status is 1:
                    if element.id.startswith("itm"):
                        items.append(element)
                    if element.id.startswith("clu"):
                        clues.append(element)
            self.items = items            
            self.clues = clues        


        def find_positions(self):
            padding = self.padding
            x = self.x
            y = self.y

            both_y = y / 4
            itm_x = padding
            clu_x = x - padding

            self.itm_coord = (itm_x, both_y)
            self.clu_coord = (clu_x, both_y)


        def draw(self):

            import pygame
            import itertools
            import os
            from os import chdir
            from os.path import dirname
            screen = self.screen
            txt_color = self.txt_color
            size = self.txt_size
            # DIRNAME = os.path.join(dirname(__file__), "resources",)

            font = pygame.font.Font(os.path.join(self.folder, "font", "advert.ttf"), size)
            
            text = font.render("ITEMS", 0, txt_color)
            rect = text.get_rect()
            rect.topleft = self.itm_coord
            screen.blit(text, rect)

            text = font.render("CLUES", 0, txt_color)
            rect = text.get_rect()
            rect.topright = self.clu_coord
            screen.blit(text, rect)            

            itm_counter = self.itm_coord[1]
            clu_counter = self.clu_coord[1]

            self.clear()

            
            for item in self.items:
                x = self.itm_coord[0]
                y = self.itm_coord[1]
                itm_counter = itm_counter + self.spacing + self.txt_size
                name = item.name
                color = item.determine_color()                
                text = font.render(name, 0, color)
                rect = text.get_rect()
                rect.topleft = (x,itm_counter)
                item.rect = rect
                self.itm_rects.append(rect)
                screen.blit(text, rect)
                

            
            for clue in self.clues:
                x = self.clu_coord[0]
                y = self.clu_coord[1]
                clu_counter = clu_counter + self.spacing + self.txt_size
                name = clue.name
                color = clue.determine_color()
                text = font.render(name, 0, color)
                rect = text.get_rect()
                rect.topright = (x,clu_counter)
                clue.rect = rect
                self.clu_rects.append(rect)
                screen.blit(text, rect)
                

        def get_collisions(self, mrect):                         #detects if the user is hovering over a wheel rectangle
            index_itm = mrect.collidelist(self.itm_rects)
            index_clu = mrect.collidelist(self.clu_rects) 
            index = None
            item = None  
            inv_type = None     
            
            if index_itm is not -1:
                item = self.items[index_itm]               
                inv_type = "itm"
                index = index_itm
                             
            if index_clu is not -1:
                item = self.clues[index_clu]
                inv_type = "clu"
                index = index_clu     

            for element in self.pool:
                element.get_collisions(mrect)       
            
            return item, index, inv_type        


        def clear(self):
            import pygame
            screen = self.screen
            for i in self.itm_rects:
                x, y, width, height = i
                surface = pygame.Surface((width, height))
                surface.fill((0,0,0))
                screen.blit(surface, (x,y))

            for i in self.clu_rects:
                x, y, width, height = i
                surface = pygame.Surface((width, height))
                surface.fill((0,0,0))
                screen.blit(surface, (x,y))

            self.itm_rects = []
            self.clu_rects = []

        def select(self, item):        
            for i in self.pool:
                if item == i.id:
                    i.selected = True
 

        def deselect(self):
            for item in self.pool:
                item.selected = False


class Item():
    def __init__(self, data, id, flags):
        self.status = 0
        self.id = id  
        self.reveal = []    
        self.data = data
        self.flags = flags
        self.update()
        self.hover = False
        self.selected = False 
        self.rect = (0,0,0,0)       
             

    def default_data(self):
        self.left = [self.id + ": left"]
        self.right = [self.id + ": right"]
        self.name = [self.id] 
        
    def set_attributes(self, data):
        for key, value in data.items():
            key = key.lower()
            setattr(self,key,value)

    def status_check(self):
        key = self.id
        operator = "="
        value = int(1)
        req = [key, operator, value]

        if self.flags.check(*req) == True:
            self.status = 1
        else:
            self.status = 0

    def format_all(self):
        self.format("name")
        self.format("left")
        self.format("right")
        self.format("reveal")
        

    def format(self, attribute):
        from tools import req_format      
        data = self.__dict__[attribute]
        output = []

        for line in data:         
            formatted_line = req_format(line)
            output.append(formatted_line)
        self.__dict__[attribute] = output

    def check(self, line):
        flags = self.flags
        reqs = line[1]
        if reqs == []:
            return True
        else:
            for req in reqs:           
                if self.flags.check(*req) == False:
                    return False
                else:
                    return True

    def finalize(self):

        for line in self.name:
            if self.check(line) == True:
                name = line[0]
        for line in self.left:
            if self.check(line) == True:
                left = line[0]
        for line in self.right:
            if self.check(line) == True:
                right = line[0]
        self.name = name
        self.left = left
        self.right = right

    def determine_color(self):
        color_text = (200, 200, 200)
        color_selected = (135, 13, 145)
        color_hover = (255, 255, 255)
        color = color_text
        if self.hover == True:        
            color = color_hover
        if self.selected == True:
            color = color_selected
        return color

    def get_collisions(self, mrect):
        if mrect.colliderect(self.rect):
            self.hover = True            
        else:
            self.hover = False
            

    def update(self):

        self.default_data()
        self.set_attributes(self.data)
        self.format_all()
        self.finalize()
        self.status_check()
        

from inventory import Item
class Clue(Item):
    pass
  
    




