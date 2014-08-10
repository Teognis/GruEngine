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

            
    def draw_triangles(self):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        screen = self.screen
        BACKGROUND = pygame.Surface(self.size)
        BACKGROUND.fill((0,0,0))
        TRIANGLE = pygame.image.load(os.path.join(self.folder, "img", "ptriangle.png"))  
        TRI_N = pygame.transform.smoothscale(TRIANGLE, (25,25))     
        TRI_NW = pygame.transform.rotate(TRI_N, 45)
        TRI_W = pygame.transform.rotate(TRI_N,90)
        TRI_SW = pygame.transform.rotate(TRI_N, 135)
        TRI_S = pygame.transform.rotate(TRI_N,180)
        TRI_SE = pygame.transform.rotate(TRI_N,225)
        TRI_E = pygame.transform.rotate(TRI_N,270)
        TRI_NE = pygame.transform.rotate(TRI_N,315)
        tri_n_coords = self.tri_coords[0]
        tri_ne_coords = self.tri_coords[1]
        tri_e_coords = self.tri_coords[2]
        tri_se_coords = self.tri_coords[3]
        tri_s_coords = self.tri_coords[4]
        tri_sw_coords = self.tri_coords[5]
        tri_w_coords = self.tri_coords[6]
        tri_nw_coords = self.tri_coords[7]
        tri_n_rect = TRI_N.get_rect()
        tri_n_rect.center = tri_n_coords
        tri_ne_rect = TRI_NE.get_rect()
        tri_ne_rect.center = tri_ne_coords
        tri_e_rect = TRI_E.get_rect()
        tri_e_rect.center = tri_e_coords
        tri_se_rect = TRI_SE.get_rect()
        tri_se_rect.center = tri_se_coords
        tri_s_rect = TRI_S.get_rect()
        tri_s_rect.center = tri_s_coords
        tri_sw_rect = TRI_SW.get_rect()
        tri_sw_rect.center = tri_sw_coords
        tri_w_rect = TRI_W.get_rect()
        tri_w_rect.center = tri_w_coords
        tri_nw_rect = TRI_NW.get_rect()
        tri_nw_rect.center = tri_nw_coords
        screen.blit(BACKGROUND, self.blank)
        screen.blit(TRI_N,tri_n_rect)
        screen.blit(TRI_NE,tri_ne_rect)
        screen.blit(TRI_E,tri_e_rect)
        screen.blit(TRI_SE,tri_se_rect)
        screen.blit(TRI_S,tri_s_rect)
        screen.blit(TRI_SW,tri_sw_rect)
        screen.blit(TRI_W,tri_w_rect)
        screen.blit(TRI_NW,tri_nw_rect)     
               
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
            text = font.render(name, 1, txtcolor)        
            rect = text.get_rect()
            rect = linkrect_position(key,rect,coord)
            self.outrects.append(rect)
            
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
            text = font.render(word, 1, txtcolor)        
            rect = text.get_rect()
            rect.center = coord
            self.inrects.append(rect)            
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

class Anchor():
    def __init__(self, data, flags):   
        self.flags = flags
        self.forward = None
        self.type = None
        self.link = None     
        self.set_attributes(data)
        self.collect_link()

                           
    def set_attributes(self, dict):
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_link(self):
        
        if self.link is not None:                  
            
            self.forward = self.link[0]
        else:
            pass

            

   
            
        
        

            
            
            
        
            




