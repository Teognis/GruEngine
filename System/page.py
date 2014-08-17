class Page():

    def __init__(self, defaults, screen, background, flags, combiner, inventory):
        import pygame
        from glyph import Editor, Glyph, Macros, Text
        self.inventory = inventory
        self.combiner = combiner
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
            
    def update(self, input, links):    
        self.glyph.clear(self.screen, self.background)
        self.glyph.input(input, justify = "justified")
        self.glyph.update()
        self.populate(links)

    def populate(self, links):        
        from page import Hyperlink
        self.hyperlinks = []
        for link in links:
            rect = self.find_rect(link[2])
            hyperlink = Hyperlink(link, rect, self.defaults, self.screen, self.glyph_rect, self.flags, self.combiner, self.inventory)
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
        mpos = pygame.mouse.get_pos()          
        self.get_collisions(mpos)  
        self.screen.blit(self.glyph.image, self.glyph_rect)
        for link in self.hyperlinks:
            link.draw()

    def get_collisions(self, mpos):
        import pygame
        mrect = pygame.Rect(mpos, (1,1))
        for hyperlink in self.hyperlinks:
            hyperlink.determine_distance(mrect)
            if mrect.colliderect(hyperlink.rect):                                
                hyperlink.hover = True               
            else:
                hyperlink.hover = False    

    def find_hover(self):
        for hyperlink in self.hyperlinks:            
            if hyperlink.hover == True:
                return hyperlink.content
            else:
                return None     


class Hyperlink():
    def __init__(self, link, rect, defaults, screen, glyph_rect, flags, combiner, inventory):   
        self.combiner = combiner
        self.flags = flags
        self.inventory = inventory     
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
        self.hover = False
        self.distance = 0
        self.visible = self.determine_visibility()       
        

    def get_position(self, glyph_rect):
        x = glyph_rect[0]
        y = glyph_rect[1]
        self.rect = self.rect.move(x,y)

    
    def draw(self): 
        import pygame 
        color = self.determine_color() 
        text = self.font.render(self.word, 2, color)
        rect = self.rect  

        blank = pygame.Surface((rect[2],rect[3]))
        blank.convert()
        blank.fill((0,0,0))     
                
        self.screen.blit(blank, rect)
        self.screen.blit(text, rect)

    def determine_color(self):
        color_text = (200, 200, 200)
        color_active = (135, 13, 145)
        color_selected = (255, 255, 255)
        if self.hover is True:
            color = color_selected      
        else:
            color = color_active

        if self.visible == False:
            color = color_text

        if self.check_clue() == True:            
            color = self.mix_color()        

        return color

    def determine_visibility(self):  
        
        if self.flags.check(self.content, "=", 1): 
            # pygame.mouse.set_cursor(*HAND_CURSOR)             
            return True
        else:             
            return False
            # pygame.mouse.set_cursor(*DEFAULT_CURSOR)  

    def determine_distance(self, mpos):
        import math
        center = self.rect.center
        link_x = center[0]
        link_y = center[1]
        mouse_x = mpos[0]
        mouse_y = mpos[1]
        distance = math.sqrt((link_x-mouse_x)**2 + (link_y-mouse_y)**2)
        distance = math.trunc(distance)
        self.distance = distance

    def check_clue(self):
        from tools import check_flags
        if len(self.combiner.box) == 1:            
            item_id = self.combiner.box[0] 
            if self.visible == False:           
                link_id = self.content
                for entity in self.inventory.pool:
                    if entity.id == item_id:
                        item = entity
                        for revealed_link in item.reveal:
                            if revealed_link[0] == link_id:
                                if check_flags(revealed_link, self.flags):
                                    return True
        else:
            return False   

    def mix_color(self): 
        if self.distance <= 55:       
            distance = 55 - self.distance
        else:
            distance = 0
        hue = 200 + distance
        color = (hue,hue,hue)        
        return color             
   

            
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
