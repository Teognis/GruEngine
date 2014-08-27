class Library():
    
    def __init__(self, main, config):
        import pygame
        self.main = main
        self.config = config
        self.screen = config.SCREEN
        self.screen_size = config.SCREEN_SIZE
        self.resource_folder = config.RESOURCES
        self.background = config.BKGSCREEN
        self.glyph_rect = pygame.Rect(0, 0, 560, 270)
        self.find_position(self.background, self.glyph_rect)  
        self.button_rect = (0,0,0,0) 
        self.button_hover = False    
        self.shelf = []
        self.selected = None
        self.find_folder()
        self.populate()
        # self.draw()

    def get_collisions(self, mrect):
        for spine in self.shelf:
            spine.get_collisions(mrect)
        if mrect.colliderect(self.button_rect):
            self.button_hover = True
        else:
            self.button_hover = False        

    def find_folder(self):
        import os
        from os import chdir
        from os.path import dirname
        LIBRARY = os.path.join(dirname(dirname(__file__)), "library")
        self.folder = LIBRARY      


    def populate(self):
        import os
        from library import Spine
        for game in os.listdir(self.folder):
            spine = Spine(game, self.folder)
            self.shelf.append(spine)

    def find_position(self, surface, rect):
        surfrect = surface.get_rect()
        rect.x = ((surfrect.w / 2) - (rect.w / 2))
        rect.y = ((surfrect.h / 2) - (rect.h / 2)) - 70 

    def draw(self):
        import os
        from os import chdir
        from os.path import dirname
        import pygame

        font_size = 16
        padding = 10        

        self.font = pygame.font.Font(os.path.join(self.resource_folder, "font", "silkscreen.ttf"), font_size)
        
             
        self.clear()
        x = self.screen_size[0]
        y = self.screen_size[1]

        offset_x = self.glyph_rect[0]
        offset_y = self.glyph_rect[1]

        # draw title

        title_text = "Library"
        title_font = pygame.font.Font(os.path.join(self.resource_folder, "font", "silkscreen.ttf"), 20)
        text = title_font.render(title_text, 0, (200,200,200))
        rect = text.get_rect()
        rect.center = (x/2, y/8)
        self.title_rect = rect
        self.screen.blit(text, rect)

        # draw a list of .gru games
       
        offset_counter = 0
        for spine in self.shelf:
            title = spine.title            
            color = spine.determine_color()
            text = self.font.render(title, 0, color)
            rect = text.get_rect()
            rect.move_ip(offset_x, offset_y)
            rect.move_ip(0, offset_counter)
            spine.rect = rect
            self.screen.blit(text, rect)
            offset_counter = offset_counter + padding + font_size
        
        offset_counter = 0
        if self.selected is not None:

            color = (201, 145, 100)
            meta_order = ["author", "release", "description"]
            for item in meta_order:
                content = self.selected.__dict__[item]
                if item == "author":
                    content = "by " + content
                text = self.font.render(content, 0, color)
                rect = text.get_rect()
                rect.topright = (x - offset_x, offset_y)
                rect.move_ip(0, offset_counter)
                self.screen.blit(text, rect)
                offset_counter = offset_counter + padding + font_size

            if self.button_hover == True:
                button_color = (255, 255, 255)
            else:
                button_color = (200, 200, 200)

            text = self.font.render("Load .gru file", 0, button_color)
            rect = text.get_rect()
            rect.center = (x/2,3*y/5)
            self.button_rect = rect
            self.screen.blit(text, rect)

    def clear(self):
        self.screen.blit(self.background, self.glyph_rect)


    
    def input(self):
        selection = self.selected
        self.selected = None
        for spine in self.shelf:
            if spine.hover == True:                
                spine.selected = True
                self.selected = spine
            else:
                spine.selected = False
        if self.button_hover == True:
            self.load(selection)
  

    def load(self, selection):
        import game
        from game import Game
        import os
        if selection == None:
            pass
        else:
            self.clear()
            self.screen.blit(self.background, self.title_rect)  
            name = selection.title  
            path = self.folder + "\\" + name + ".gru"        
            game = Game(path)
            self.main.load(game)
        

class Spine():

    def __init__(self, gru_file, folder):
        self.gru_file = gru_file
        self.folder = folder
        self.set_defaults()
        self.pull_metadata()
        self.rect = (0,0,0,0)
        self.hover = False
        self.selected = False
    
    def set_defaults(self):
        self.title = str(self.gru_file)
        self.author = "Author unknown"
        self.description = "Stuff happens"
        self.release = "Date unknown"


    def pull_metadata(self):
        import os
        from os import chdir
        from os.path import dirname
        import yaml
        gru_file = open(os.path.join(self.folder, self.gru_file), "r")
        data = yaml.load(gru_file)
        metadata = data["metadata"]
        self.__dict__.update(metadata)
        self.metadata = metadata.items()
        gru_file.close()

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

