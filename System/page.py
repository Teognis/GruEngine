class Page():

    def __init__(self, defaults, screen, background, flags):
        import pygame
        # import glyph
        from glyph import Editor, Glyph, Macros, Text
        self.flags = flags
        self.defaults = defaults
        self.screen = screen
        self.background = background
        self.glyph_rect = pygame.Rect(0, 0, 560, 270)
        self.find_position(self.background, self.glyph_rect)       
        self.glyph = Glyph(self.glyph_rect, **self.defaults)              
        self.glyph.image.set_alpha(255)
        
        Macros["default"] = ("color", (200, 200, 200)) 
        

    def find_position(self, surface, rect):
        surfrect = surface.get_rect()
        rect.x = ((surfrect.w / 2) - (rect.w / 2))
        rect.y = ((surfrect.h / 2) - (rect.h / 2)) - 70 
            

    def find_macros(self, text):

        color_text = (200, 200, 200)
        color_active = (135, 13, 145)
        color_selected = (255, 255, 255)

        self.glyph.Macros = {}           
        text = text.split()
        Macros = {}
        macros = []
        for word in text:
            if word.startswith("lnk_"):
                word = word.rstrip(";")
                macros.append(word)
        for link in macros:
            if self.state.flags.check(link, "=", 1):
                color = color_active
            else:
                color = color_text            
            Macros[link] = ("color", color) 
        return Macros
        # print self.glyph.Macros 

    def update(self, input, links):    
        self.glyph.clear(self.screen, self.background)
        self.glyph.input(input, justify = "justified")
        self.glyph.update()
        self.populate(links)

    def populate(self, links):        
        from page import Hyperlink
        self.hyperlinks = []
        for link in links:
            rect = self.find_rect(link[1])
            hyperlink = Hyperlink(link, rect, self.defaults, self.screen, self.glyph_rect, self.flags)
            self.hyperlinks.append(hyperlink)

    def find_rect(self, link):
        # print link
        rect = None
        for item in self.glyph.links.items():            
            if item[0] == link:
                rect = item[1][0]
                return rect          
        
    def draw(self):
        import pygame
        self.screen.blit(self.glyph.image, self.glyph_rect)
        for link in self.hyperlinks:
            link.draw()


class Hyperlink():
    def __init__(self, link, rect, defaults, screen, glyph_rect, flags):        
        self.word = link[0]
        self.content = link[1]
        self.rect = rect
        self.color_hidden = (200,200,200)
        self.color_hover = (255,255,255)
        self.color_default = (135, 13, 145)
        self.defaults = defaults
        self.screen = screen
        self.font = self.defaults["font"]
        self.get_position(glyph_rect)
        

    def get_position(self, glyph_rect):
        x = glyph_rect[0]
        y = glyph_rect[1]
        self.rect = self.rect.move(x,y)

    
    def draw(self): 
        import pygame  
        color = self.color_default 
        color = self.color_hidden
         

        text = self.font.render(self.word, 2, color)
        rect = self.rect  
        blank = pygame.Surface((rect[2],rect[3]))
        blank.convert()
        blank.fill((0,0,0))        
        # blank = pygame.Surface.fill(0,0,0)        
        
        self.screen.blit(blank, rect)
        self.screen.blit(text, rect)

    def determine_color(self):
        pass
        

    def get_collisions(self):
        pass


            # LINKS =  find_links(glyph)  
            # PROX = link_distance(LINKS,mpos)
            # lnk_click = glyph.get_collisions(mouse.get_pos())
            # menu_click = menu.get_collisions(mrect)               
            # whl_click = wheel.get_collisions(mrect)  
            # inv_click = inventory.get_collisions(mrect)
                            
            # if lnk_click:              
            #     glyph_draw(state.output, lnk_click, flags)   
            #     if flags.check(lnk_click, "=", 1): mouse.set_cursor(*HAND_CURSOR)                                
            # else:             
            #     glyph_draw(state.output, None, flags)
            #     mouse.set_cursor(*DEFAULT_CURSOR)
            # SCREEN.blit(glyph.image, glyph_rect) 

            # if inv_click[0] is not None: state.inventory.draw_selection(*inv_click)
            # if menu_click is not None: menu.draw_selection(menu_click)
