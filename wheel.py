class Wheel():
 
    def __init__(self, size):                               #creates and instance of a Wheel (that takes into account the screen coordinates)
        self.inrects = []
        self.outrects = []
        self.padding = 60
        self.x = size[0]
        self.y = size[1]
        self.find_positions()
        self.focus = "Inner"
        self.state = []
        self.inner = ["Use","Attack","Evade","Defend"]
        self.ypos = 650
        self.exit_color = (201, 145, 100)
        self.button_color = (200, 168, 200)
        self.exit_size = 14
        self.button_size = 17
        
##        self.linkpos = [(self.x/2,self.ypos + 50),(self.x/2 + 30,self.ypos + 30),(self.x/2 + 60,self.ypos),(self.x/2 + 30,self.ypos - 30),(self.x/2,self.ypos - 50),(self.x/2 - 30,self.ypos - 30),(self.x/2 - 60,self.ypos),(self.x/2 - 30,self.ypos + 30)]
        
        
          
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
        self.blank = [(0,y_top),(y-y_top,x)]
        self.coords = [(x_mid, y_upper),(x_right, y_mid),(x_mid, y_lower),(x_left, y_mid)]
        link_coords = [(x_mid, y_top - l_step),(x_right + l_step, y_upper - l_step),(x_rightest + l_step, y_mid),(x_right + l_step, y_lower + l_step),(x_mid, y_bot + l_step),(x_left - l_step, y_lower + l_step),(x_leftest - l_step, y_mid),(x_left - l_step, y_upper - l_step)]
        self.linkpos = link_coords

            
    def draw_triangles(self, screen):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        DIRNAME = os.path.join(dirname(__file__), "resources",)
        BKGSCREEN = pygame.image.load(os.path.join(DIRNAME, "img", "bkgscreen.tga"))
        BKGSCREEN = pygame.transform.scale(BKGSCREEN, (self.x,self.y))
        BKGSCREEN = BKGSCREEN.convert()
        BKGSCREEN.fill((0,0,0))
        TRIANGLE = pygame.image.load(os.path.join(DIRNAME, "img", "ptriangle.png"))
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
        screen.blit(BKGSCREEN,self.blank)
        screen.blit(TRI_N,tri_n_rect)
        screen.blit(TRI_NE,tri_ne_rect)
        screen.blit(TRI_E,tri_e_rect)
        screen.blit(TRI_SE,tri_se_rect)
        screen.blit(TRI_S,tri_s_rect)
        screen.blit(TRI_SW,tri_sw_rect)
        screen.blit(TRI_W,tri_w_rect)
        screen.blit(TRI_NW,tri_nw_rect)
        
       
        
    def draw_exits(self, screen):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        txtcolor = self.exit_color
        DIRNAME = os.path.join(dirname(__file__), "resources",)
        font = pygame.font.Font(os.path.join(DIRNAME, "font", "advert.ttf"), self.exit_size)

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
            name = self.links[key].name
            text = font.render(name, 1, txtcolor)        
            rect = text.get_rect()
            rect = linkrect_position(key,rect,coord)
            self.outrects.append(rect)
            screen.blit(text, rect)

    def draw_buttons(self, screen):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        DIRNAME = os.path.join(dirname(__file__), "resources",)        
        txtcolor = self.button_color        
##      txtcolor = (201, 192, 187)        
        font = pygame.font.Font(os.path.join(DIRNAME, "font", "advert.ttf"), self.button_size)      
        for word, coord in zip(self.inner,self.coords):            
            text = font.render(word, 1, txtcolor)        
            rect = text.get_rect()
            rect.center = coord
            self.inrects.append(rect)
            screen.blit(text, rect)              
        
    def draw(self, screen):
        self.draw_triangles(screen)
##        self.draw_buttons(screen)
##        self.draw_exits(screen)       
        

    def state_back(self):                                   #this "undo" function deletes the last wheel command from the stack
        if len(self.state) is not 0:
            self.state.pop()
        

    def input(self, direction):                             #enters the (already parsed) keyboard/mouse commands into the self.state stack
        if direction == 0:
            self.state_back()
        if len(self.state) < 3:
            self.state.append(direction)

    def get_collisions(self, mrect):                         #detects if the user is hovering over a wheel rectangle
        index_in = mrect.collidelist(self.inrects)
        index_out = mrect.collidelist(self.outrects)
        if index_in is not -1:
            return index_in
        elif index_out is not -1:
            return index_out           
        
        
    def set_exits(self, room):
        exits = []
        for exit in room.exits:
            exits.append(exit)
        self.exits = exits 
           
    def find_coords(self, room):
        coord = room.coord
        exits = self.exits
        links = {}
        
        def neighbour_list(coord):
            coords = []
            x = coord[0]
            y = coord[1]
            seq = [(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1)]
            coords.extend(seq)
            return coords
        neighbours = neighbour_list(coord)

        for i in exits:
            if i.coord in neighbours:
                index = neighbours.index(i.coord)
                links[index] = i
        self.links = links
            
            
        
            





    

        
              
        
       
