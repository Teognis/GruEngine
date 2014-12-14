class Dispatcher():

    def __init__(self, collider, library, menu, game=None):
        self.library = library
        self.menu = menu
        self.game = game
        self.collider = collider

    def process(self, event):
        import pygame        
        ev = event        
        ev_type = pygame.event.event_name(ev.type)
        
        if ev_type == "MouseButtonDown":
            if ev.button == 1:
                self.library.input()                      
                self.menu.input(self.collider.get(), "left", "down")
            if ev.button == 3:
                self.menu.input(self.collider.get(), "right", "up")           

        if ev_type == "MouseButtonUp":
            if ev.button == 1:
                self.menu.input(self.collider.get(),"left", "up")
            if ev.button == 3: 
                self.menu.input(self.collider.get(),"right", "up")
                                     
        if ev_type == "Keydown": 
            if ev.key == "K_Escape": 
                if self.menu.focus == None: 
                    exit() 
                else:
                    self.menu.enter(ev.key)                        
            else:                                            
                menu.enter(ev.key)  

