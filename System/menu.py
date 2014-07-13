class Menu():
    def __init__(self, screen, size, resource_folder, save_folder, state):
        self.state = state
        self.resource_folder = resource_folder
        self.save_folder = save_folder
        self.screen = screen
        self.x = size[0]
        self.y = size[1]
        self.padding = 30
        self.spacing = 25
        self.txt_color = (48, 48, 48)
        self.overlay_color = (201, 192, 187)
        self.focus_color = (201, 145, 100)
        self.txt_size = 16
        self.text = ["New game", "Save", "Restore", "Quit"]
        self.rects = []
        self.find_positions()
        self.focus = None
        self.save = []
        self.restore = []
        self.input_rect = []

    def find_length(self, text):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        font = pygame.font.Font(os.path.join(self.resource_folder, "font", "advert.ttf"), self.txt_size)         
        text = font.render(text, 0, self.txt_color)
        rect = text.get_rect()
        length = rect[2]
        return length       

    def find_positions(self):

        x = self.x
        y = 0 + self.spacing
        spacing = self.spacing
        padding = self.padding
        coords = []

        new_game = (padding,y)
        coords.append(new_game)
        length = self.find_length("New game")

        save_game = (new_game[0]+ length + padding, y)
        coords.append(save_game)
        length = self.find_length("Save")

        restore_game = (save_game[0] + length + padding, y)
        coords.append(restore_game)

        quit_game = (x-padding, y)
        coords.append(quit_game)

        self.coords = coords
        self.save_coord = (save_game[0], save_game[1] + spacing)
        self.restore_coord = (restore_game[0], restore_game[1] + spacing) 

    def clear(self):
        import pygame
        screen = self.screen
        for rect in self.input_rect:
            x, y, width, height = rect
            surface = pygame.Surface((width, height))
            surface.fill((0,0,0))
            screen.blit(surface, (x,y))

    def draw(self):

        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        screen = self.screen
        font = pygame.font.Font(os.path.join(self.resource_folder, "font", "advert.ttf"), self.txt_size)
        counter = 0
        rects = []
        self.clear()
        for item in self.text:       
            text = font.render(item, 0, self.txt_color)
            rect = text.get_rect()
            if item is not "Quit":
                rect.topleft = self.coords[counter]
            else:
                rect.topright = self.coords[counter]
            rects.append(rect)
            screen.blit(text, rect)
            counter += 1
        self.rects = rects
        self.draw_input()
        self.draw_focus()

    def get_collisions(self, mrect):                         #detects if the user is hovering over a wheel rectangle
        index = mrect.collidelist(self.rects)
        if index is not -1:
            return index

    def draw_selection(self, index):
        import pygame
        import os
        from os import chdir
        from os.path import dirname
        font = pygame.font.Font(os.path.join(self.resource_folder, "font", "advert.ttf"), self.txt_size)
        color = self.overlay_color
        screen = self.screen
        rect = self.rects[index]
        text = self.text[index]
        text = font.render(text, 0, color)  
        screen.blit(text, rect)

    def draw_focus(self):
        import pygame
        import os
        from os import chdir
        from os.path import dirname
        if self.focus is not None:
            if self.focus == "save":
                index = 1
            elif self.focus == "restore":
                index = 2
            font = pygame.font.Font(os.path.join(self.resource_folder, "font", "advert.ttf"), self.txt_size)
            color = self.focus_color
            screen = self.screen
            rect = self.rects[index]
            text = self.text[index]
            text = font.render(text, 0, color)  
            screen.blit(text, rect)

    def set_focus(self, index):
        if index == 0:
            pass
        if index == 1:
            self.focus = "save"
        elif index == 2:
            self.focus = "restore"
        elif index == 3:
            pass
        else:
            self.focus = None

    def input(self, key):
        import pygame
        key = pygame.key.name(key)
        focus = self.focus
        text = []
        if focus is not None:
            if key == "escape":
                self.__dict__[focus] = []
                self.focus = None
            elif key == "space":
                self.__dict__[focus].append(" ")
            elif key == "backspace":
                if len(self.__dict__[focus]) is not 0:
                    self.__dict__[focus].pop()
            elif key == "return":
                filename = self.get_text()
                if focus == "save":
                    self.save_state(filename)
                elif focus == "restore":
                    self.restore_state(filename)
                self.__dict__[focus] = []
                self.focus = None     
            else:            
                self.__dict__[focus].append(key)
    
    def get_text(self):
        text = ""
        focus = self.focus
        for key in self.__dict__[focus]:
            text = text+key
        return text


    def draw_input(self):
        import pygame
        import itertools
        import os
        from os import chdir
        from os.path import dirname
        focus = self.focus        
        if focus is not None:
            text = self.get_text()

            font = pygame.font.Font(os.path.join(self.resource_folder, "font", "advert.ttf"), self.txt_size)
            surf = font.render(text, 0, self.focus_color)  
            rect = surf.get_rect()
            if focus == "save":
                rect.topleft = self.save_coord
            elif focus == "restore":
                rect.topleft = self.restore_coord
            self.input_rect.append(rect)
            
            self.screen.blit(surf, rect) 

    def save_state(self, filename):
        import os
        from os import chdir
        from os.path import dirname
        newname = filename + ".txt"
        file_path = os.path.join(self.save_folder, newname)
        f = open(file_path, "w")   
        f.write( "SAVED STATE")    
        f.close()

    def restore_state(self, filename):
        import os
        from os import chdir
        from os.path import dirname
        newname = filename + ".txt"
        file_path = os.path.join(self.save_folder, newname)
        if os.path.isfile(file_path) is True:       
            f = open(file_path, "r")  
            for i in f.readlines():
                print i
            f.close()
        else:
            print "File " + newname + " does not exist!"
        






        


    
