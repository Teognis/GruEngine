class Wheel():
 
    def __init__(self, screen, size, folder):
        #creates an instance of a Wheel (that takes into account the screen coordinates)
       
        self.folder = folder
        self.links = []
        self.screen = screen
        self.size = size
        self.inrects = []
        self.outrects = []
        self.padding = 60 
        self.anchor = None     
        self.x = size[0]
        self.y = size[1]
        self.find_positions()
        self.prepare_triangles()
        self.focus = "Inner"
        self.state = []
        self.ypos = 650
        self.exit_color = (201, 145, 100)
        self.button_color = (200, 168, 200)
        self.exit_size = 14
        self.button_size = 17
        self.scene = None
               
          
    def find_positions(self):                   #automatically finds coordinates for triangles, links, buttons, etc.
        padding = self.padding
        y = self.y - padding
        x = self.x
        x_step = x/18
        y_step = y/16
        l_step = 16
        
        center_x = x/2
        center_y = 3*y/4 + y/8 
        self.wheel_x = center_x
        self.wheel_y = center_y
        y_top = center_y - 2 * y_step
        y_upper = center_y - y_step
        y_mid = center_y
        y_lower = center_y + y_step
        y_bot = center_y + 2 * y_step
        x_leftest = center_x - 2 * x_step
        x_left = center_x - x_step
        x_mid = center_x
        x_right = center_x + x_step
        x_rightest = center_x + 2 * x_step
        tri_coords = [(x_mid,y_top), (x_right,y_upper),(x_rightest,y_mid),(x_right,y_lower),(x_mid,y_bot),(x_left,y_lower),(x_leftest,y_mid),(x_left,y_upper)]
        self.tri_coords = tri_coords
        self.blank = [(0,y_top - padding),(y-y_top,x)]        
        self.coords = [(x_mid, y_upper),(x_right, y_mid),(x_mid, y_lower),(x_left, y_mid)]
        link_coords = [(x_mid, y_top - l_step),(x_right + l_step, y_upper - l_step),(x_rightest + l_step, y_mid),(x_right + l_step, y_lower + l_step),(x_mid, y_bot + l_step),(x_left - l_step, y_lower + l_step),(x_leftest - l_step, y_mid),(x_left - l_step, y_upper - l_step)]
        self.linkpos = link_coords

    def prepare_triangles(self):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname

        TRIANGLE = pygame.image.load(os.path.join(self.folder, "img", "ptriangle.png"))  
        N = pygame.transform.smoothscale(TRIANGLE, (25,25))     
        NW = pygame.transform.rotate(N, 45)
        W = pygame.transform.rotate(N,90)
        SW = pygame.transform.rotate(N, 135)
        S = pygame.transform.rotate(N,180)
        SE = pygame.transform.rotate(N,225)
        E = pygame.transform.rotate(N,270)
        NE = pygame.transform.rotate(N,315)
        tri = [N, NE, E, SE, S, SW, W, NW]

        counter = 0
        triangles = []
        for triangle in tri:

            triangle_rect = triangle.get_rect()
            triangle_rect.center = self.tri_coords[counter]
            triangle = triangle, triangle_rect
            triangles.append(triangle)
            counter += 1
        self.triangles = triangles
        
       

            
    def draw_triangles(self):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
    
        screen = self.screen
        BACKGROUND = pygame.Surface(self.size)
        BACKGROUND.fill((0,0,0))
 
        screen.blit(BACKGROUND, self.blank)
        for triangle in self.triangles:
            surface, rect = triangle
            screen.blit(surface, rect)
               
    def draw_exits(self):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        screen = self.screen
        txtcolor = self.exit_color
        font = pygame.font.Font(os.path.join(self.folder, "font", "advert.ttf"), self.exit_size)

        def linkrect_position(key, rect, coord):
            if key == 0:
                rect.midbottom = coord
            elif key == 1:
                rect.bottomleft = coord
            elif key == 2:
                rect.midleft = coord
            elif key == 3:
                rect.topleft = coord
            elif key == 4:
                rect.midtop = coord
            elif key == 5:
                rect.topright = coord
            elif key == 6:
                rect.midright = coord
            elif key == 7:
                rect.bottomright = coord
            return rect
                
        
        for key in self.links:           

            coord = self.linkpos[key]
            name = self.links[key].txt 
            color = self.links[key].determine_color()           
            text = font.render(name, 1, color)        
            rect = text.get_rect()
            rect = linkrect_position(key,rect,coord)
            self.outrects.append(rect)
            self.links[key].rect = rect            
            screen.blit(text, rect)

    def draw_button(self):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        screen = self.screen
        DIRNAME = os.path.join(dirname(__file__), "resources",)        
        txtcolor = self.button_color 
        coord = (self.wheel_x, self.wheel_y)    
        font = pygame.font.Font(os.path.join(self.folder, "font", "advert.ttf"), self.button_size)      
        
        
        if self.scene.anchor is not None:            
            word = self.scene.anchor.type
            color = self.scene.anchor.determine_color()
            text = font.render(word, 1, color)        
            rect = text.get_rect()
            rect.center = coord
            self.inrects.append(rect) 
            self.scene.anchor.rect = rect           
            screen.blit(text, rect)    

                                      
        
    def draw(self):
        self.draw_triangles()
        self.draw_button()
        self.draw_exits()       
        

    def get_collisions(self, mrect):                         #detects if the user is hovering over a wheel rectangle
        index_in = mrect.collidelist(self.inrects)
        index_out = mrect.collidelist(self.outrects)        
        
        w_button = None
             
        if index_out is not -1:
            items = self.links.keys()   
            # print items, index_out         
            w_button = items[index_out]  
            w_button = "whl_" + str(w_button)          

                     
        if index_in is not -1:
            w_button = self.button.type
            w_button = "whl_" + w_button
       

        for wlink in self.links:
            self.links[wlink].get_collisions(mrect)

        if self.button is not None:
            self.button.get_collisions(mrect)
       

        return w_button
                      
           

    def update(self, scene):           
        # self.clear() 
        self.scene = scene 
        self.inrects = []
        self.outrects = []   
        self.links = scene.links     
        self.button = scene.anchor     
         
             
                    
    def clear(self):
        # self.links = {}        
        
        import pygame
        screen = self.screen
        for i in self.inrects:
            x, y, width, height = i
            surface = pygame.Surface((width, height))
            surface.fill((0,0,0))
            screen.blit(surface, (x,y))

        for i in self.outrects:
            x, y, width, height = i
            surface = pygame.Surface((width, height))
            surface.fill((0,0,0))
            screen.blit(surface, (x,y))

        self.inrects = []
        self.outrects = []


class Wlink():

    def __init__(self, data, flags):                       #creates an instance of a wheel link (which holds its name and both link paths)
        self.flags = flags
        self.txt = None
        self.left = None
        self.right = None            
        self.set_attributes(data) 
        self.output("txt")
        self.output("left")
        self.output("right")       
        self.rect = [0,0,0,0]
        self.hover = False
        
    
    def output(self, attribute):
        if getattr(self, attribute) is not None:
            self.format(attribute)
            self.set(attribute)

    def set(self, attribute):
        import copy
        data = self.__dict__[attribute]        
        output = None
        for line in data:
            if self.check(line):
                output = line[0]
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
    
    def format(self, attribute):
        from tools import req_format      
        data = self.__dict__[attribute]
        output = []
        for line in data:
            formatted_line = req_format(line)
            output.append(formatted_line)
        self.__dict__[attribute] = output

    def set_attributes(self, data):                 #generates attributes out of yml streeam
        for key, value in data.items():
            key = key.lower()
            setattr(self,key,value)

    def get_collisions(self, mrect):
        if mrect.colliderect(self.rect):
            self.hover = True
        else:
            self.hover = False

    def determine_color(self):
        color = (201, 145, 100)
        if self.hover == True:
            color = (255,255,255)
        return color
        

class Anchor():
    def __init__(self, data, flags):   
        self.flags = flags
        self.forward = None
        self.type = None
        self.link = None     
        self.set_attributes(data)
        self.collect_link()
        self.rect = [0,0,0,0]
        self.hover = False

                           
    def set_attributes(self, dict):
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_link(self):
        
        if self.link is not None:                  
            
            self.forward = self.link[0]
        else:
            pass

    def determine_color(self):
        color = (200, 200, 200)
        if self.hover == True:
            color = (255,255,255)
        return color
    
    def get_collisions(self, mrect):
        if mrect.colliderect(self.rect):
            self.hover = True
        else:
            self.hover = False 

            

   
            
        
        

            
            
            
        
            




