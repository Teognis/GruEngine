class Collider():
    import pygame
    
    def __init__(self,page,menu,wheel,inventory):
        self.page = page
        self.glyph = self.page.glyph
        self.menu = menu
        self.wheel = wheel
        self.inventory = inventory        
        self.click_id = None
        self.click_type = None        

    def get(self):
        self.check()        
        return self.click_id, self.click_type

    def determine_input(self, l_click, w_click, i_click, m_click):
        input_type = None
        input_id = None
        if l_click is not None:
            input_id = l_click
            input_type = "lnk"
        if w_click is not None:
            input_id = w_click
            input_type = "whl"
        if i_click[0] is not None:
            input_id = i_click[0].id
            input_type = "inv"
        if m_click is not None:
            input_id = self.menu.menu_id[m_click]
            input_type = "mnu"            
        return input_id, input_type

    def check(self):
        import pygame
        mouse = pygame.mouse
        mpos = pygame.mouse.get_pos()
        mrect = pygame.Rect(mpos, (1,1))         

        link_id = self.glyph.get_collisions(mouse.get_pos())       
        wheel_id = self.wheel.get_collisions(mrect)          
        inventory_id = self.inventory.get_collisions(mrect)
        menu_id = self.menu.get_collisions(mrect)       
        
        self.click_id, self.click_type = self.determine_input(link_id, wheel_id,inventory_id, menu_id)

        

