class Collider():
    import pygame
    
    def __init__(self,page,menu,wheel,inventory,flags):
        self.page = page
        self.glyph = self.page.glyph
        self.menu = menu
        self.wheel = wheel
        self.inventory = inventory
        self.flags = flags 
        self.build_cursor()       
        self.click_id = None
        self.click_type = None        

    def get(self):
        # self.check()        
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

        # link_id = self.glyph.get_collisions(mouse.get_pos())       
        wheel_id = self.wheel.get_collisions(mrect)          
        inventory_id = self.inventory.get_collisions(mrect)
        menu_id = self.menu.get_collisions(mrect)
        link_id = self.page.find_hover()
        
        self.click_id, self.click_type = self.determine_input(link_id, wheel_id,inventory_id, menu_id)
        self.set_cursor(self.click_id, self.click_type)
    
    def set_cursor(self, hover_id, hover_type):
        from tools import check_flags
        import pygame
        show = False
        if hover_type is not None:
            show = True            
            if hover_type == "lnk":
                show = True
                if self.flags.check(hover_id,"=",1) == False:
                    show = False                    
                for item in self.inventory.pool:
                    if item.selected == True:
                        for revealed_link in item.reveal:
                            if revealed_link[0] == hover_id:                                    
                                if check_flags(revealed_link, self.flags) == True:
                                    show = True                                                                   
        if show == True:
            pygame.mouse.set_cursor(*self.cursor_hand)
        else:
            pygame.mouse.set_cursor(*self.cursor_default)

    def build_cursor(self):
        import pygame
        DEFAULT_CURSOR = pygame.mouse.get_cursor()
        _HAND_CURSOR = (
        "     XX         ",
        "    X..X        ",
        "    X..X        ",
        "    X..X        ",
        "    X..XXXXX    ",
        "    X..X..X.XX  ",
        " XX X..X..X.X.X ",
        "X..XX.........X ",
        "X...X.........X ",
        " X.....X.X.X..X ",
        "  X....X.X.X..X ",
        "  X....X.X.X.X  ",
        "   X...X.X.X.X  ",
        "    X.......X   ",
        "     X....X.X   ",
        "     XXXXX XX   ")
        _HCURS, _HMASK = pygame.cursors.compile(_HAND_CURSOR, ".", "X")
        HAND_CURSOR = ((16, 16), (5, 1), _HCURS, _HMASK)
        self.cursor_default = DEFAULT_CURSOR
        self.cursor_hand = HAND_CURSOR

        

