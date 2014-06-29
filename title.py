class Title():
    def __init__(self, screen, size):               
        self.screen = screen
        self.size = size
        self.find_position()
        self.text = None
        self.color = (255, 255, 255)

    def find_position(self):
        screen_x = self.size[0]
        screen_y = self.size[1]
        self.x = screen_x / 2
        self.y = screen_y / 10

    def update(self, name):
        self.clear()
        self.name = name


    def draw(self):
        import pygame 
        import os
        from os import chdir
        from os.path import dirname
        DIRNAME = os.path.join(dirname(__file__), "resources",) 
        font = pygame.font.Font(os.path.join(DIRNAME, "font", "advert.ttf"), 14)  
        screen = self.screen    
        name = self.name  
        txtcolor = self.color 
        coord = (self.x,self.y)     
        text = font.render(name, 0, txtcolor) 
        self.text = text
        rect = text.get_rect()
        rect.center = coord     
        screen.blit(text, rect)

    def clear(self):
        import pygame
        screen = self.screen
        if self.text is not None:
            rect = self.text.get_rect()            
            x, y, width, height = rect
            surface = pygame.Surface((width, height))
            surface.fill((0,0,0))
            rect.center = (self.x, self.y)            
            screen.blit(surface, rect)
