class Fps():

    def __init__(self, clock, config):
        self.clock = clock
        self.coords = config.CLOCK_POS  
        self.font = config.FONT  
        self.color = config.CLOCK_COLOR
        self.screen = config.SCREEN
        self.clear_surface()  

    def draw(self):
        
        time = self.clock.get_fps()
        txt = str(time)
        time_text = self.font.render(txt, 0, self.color)
        self.screen.blit(self.blank, (self.coords))
        self.screen.blit(time_text, (self.coords))


    def clear_surface(self):
        txt = "00000000000000"
        clear_text = self.font.render(txt, 0, self.color)
        clear_text.fill((0,0,0))
        self.blank = clear_text
