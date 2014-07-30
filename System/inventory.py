class Inventory():

        def __init__(self, itm_data, clu_data, flags, screen, size, folder):
            self.folder = folder
            self.itm_data = itm_data
            self.clu_data = clu_data
            self.flags = flags            
            self.screen = screen
            self.size = size

            self.x = size[0]
            self.y = size[1]
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
                text = font.render(name, 0, txt_color)
                rect = text.get_rect()
                rect.topleft = (x,itm_counter)
                self.itm_rects.append(rect)
                screen.blit(text, rect)

            for clue in self.clues:
                x = self.clu_coord[0]
                y = self.clu_coord[1]
                clu_counter = clu_counter + self.spacing + self.txt_size
                name = clue.name
                text = font.render(name, 0, txt_color)
                rect = text.get_rect()
                rect.topright = (x,clu_counter)
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
                    
            return item, index, inv_type

        def draw_selection(self, item, index, inv_type):
            import pygame
            import itertools
            import os
            from os import chdir
            from os.path import dirname
            font = pygame.font.Font(os.path.join(self.folder, "font", "advert.ttf"), self.txt_size)
            color = (135,13,145)
            screen = self.screen
            text = item.name
            if inv_type == "itm":
                rects = self.itm_rects
            elif inv_type == "clu":
                rects = self.clu_rects
            rect = rects[index]
            text = font.render(text, 0, color)  
            screen.blit(text, rect)          


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

class Item():
    def __init__(self, data, id, flags):
        self.status = 0
        self.id = id  
        self.reveal = []    
        self.data = data
        self.flags = flags
        self.update()        
             

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


    def update(self):

        self.default_data()
        self.set_attributes(self.data)
        self.format_all()
        self.finalize()
        self.status_check()
        

from inventory import Item
class Clue(Item):
    pass
  
    




