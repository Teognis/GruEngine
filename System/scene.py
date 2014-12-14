class Scene():  

    def __init__(self, name, data, flags):
        import copy     
        self.raw = "" 
        self.name = name
        self.data = copy.deepcopy(data)        
        self.title = "" 
        self.wheel = {}  
        self.flags = flags
        self.links = {}
        self.cutscenes = []
        self.effects = []
        self.segments = []
        self.variations = []
        self.anchor = None
        self.set_attributes(self.data)                      
        self.collect()
        self.finalize()
     
    def collect(self):
        self.collect_segments()
        self.collect_variations()
        self.collect_effects()
        self.collect_wheel()
        self.collect_anchor()
        self.collect_cutscenes()
        
    def set_attributes(self, data):         #pulls data out of the items.yml stream and configures the attributes of the Ability instance
        for key, value in data.items():        
            key = key.lower()
            setattr(self,key,value)

    def collect_segments(self):
        segments = []        
        for i in self.output:
            segments.append(i)            
        self.segments = segments
        
    def collect_variations(self):
        from scene import Line        
        segments = self.segments
        segpool = []
        for segment in segments:
            varpool = []
            for variation in segment:
                var = Line(variation, self.flags)
                varpool.append(var)
            segpool.append(varpool)
        self.pool = segpool

    def collect_effects(self):
        from tools import list_effs, format_effs
        if self.effects == []:
            pass
        else:
            self.effects = list_effs(self.effects)
            self.effects = format_effs(self.effects)

    def collect_anchor(self):             
        from wheel import Anchor
        if self.data.has_key("anchor"):        
            self.anchor = Anchor(self.anchor, self.flags)
        else:
            pass

    def collect_cutscenes(self):
        from scene import Cutscene
        self.cutscenes = Cutscene(self.cutscenes, self.flags)              
           
    def collect_wheel(self):
        
         
        def create_wlinks(data):
            from wheel import Wlink
            wheeldata = {}
            items = data.items()
            for key, value in items:           
                wlink = Wlink(value, self.flags)
                wheeldata[key] = wlink
            return wheeldata       
        wlinks = create_wlinks(self.wheel)        
        self.links.update(wlinks)

        
    def finalize(self):
        from tools import glyph_links, hide_link                    
        output = ""
        effects = self.effects
        pool = self.pool  
        padding = "/n" 

        for segment in pool:
            seg_output = ""
            seg_effects = []

            for variation in segment:
                if variation.output is not None:
                    seg_output = variation.output
                    seg_effects = variation.effects            

            output = output + padding + seg_output + padding
            # output = output + padding + seg_output          
            effects = effects + seg_effects
                
        self.effects = effects
        self.auto_flag()
        for effect in self.effects:
            self.flags.set(*effect)

        self.raw = self.find_raw(output)

        output, hyperlinks = glyph_links(output, self.flags)
        self.output = output
        self.hyperlinks = hyperlinks

    def find_raw(self, text):
        linklist = []
        tuples = []
    
        splittext = text.split(">")                 
        for i in splittext:
            indeks = i.find("<")
            if indeks is not -1:
                length = len(i)
                word = i[indeks+1:length]                    
                if word not in linklist:                     
                    linklist.append(word)
        for i in linklist:
            tpl = i.split("/")
            tuples.append(tpl)    
            counter = 0
        for i in tuples:
            word = i[0]
            link = i[1]
            index = str(counter) 
            i.append(index)              
            original = word + "/" + link
            oldstring = "<" + original + ">"   
            newstring = word  
            text = text.replace(oldstring, newstring)     
            counter += 1
        # text = text.replace("/n/n","/n")
        # text = text.replace("  "," ")
        # text = text.strip()
        text = text.replace("/n"," /n ")
        # text = text.replace("/n",'\n')
        

        return text
    
    def auto_flag(self):
        name = self.name
        effect = [name, "=", "1"]
        self.effects.append(effect)
        



class Line():
    def __init__(self, data, flags):
        self.flags = flags
        self.output = None
        self.effects = None        
        self.txt = ""
        self.req = ""
        self.eff = ""        
        self.set_attributes(data)
        self.format("req")
        self.format("eff")            
        self.finalize()       
        
     
    def set_attributes(self, data):
        for key, value in data.items():
            key = key.lower()
            setattr(self,key,value)

    def format(self, attribute):
        from tools import list_reqs, format_reqs, list_effs, format_effs      
        data = self.__dict__[attribute]
        if attribute == "req":
            list_data = list_reqs(data)
            formatted_data = format_reqs(list_data)
        elif attribute == "eff":
            list_data = list_effs(data)
            formatted_data = format_effs(list_data)
        self.__dict__[attribute] = formatted_data
        
    def check(self):
           
        for req in self.req:
            if self.flags.check(*req) == False:
                return False
            else:
                return True
        return True
    def txt_format(self):
        pass
        # self.txt = self.txt.replace(";",":")
        # self.txt = self.txt.replace("::", ";")
        

    def finalize(self):
        self.effects = self.eff  
                   
        if self.check() == True:
            self.txt_format()
            self.output = self.txt
            
class Link():

    def __init__(self, name, data, flags):
        import copy        
        self.name = name
        self.left = []
        self.right = []
        self.data = copy.deepcopy(data[name])     
        self.flags = flags
       
        self.set_attributes(self.data)
        self.format("left")
        self.format("right")        
        self.finalize()
        
    
    def set_attributes(self, data):              
        for key, value in data.items():
            key = key.lower()
            setattr(self,key,value)

    def format(self, attribute):
        from tools import req_format      
        data = self.__dict__[attribute]
        output = []
        for line in data:
            formatted_line = req_format(line)
            output.append(formatted_line)
        self.__dict__[attribute] = output

    def check(self, line):
        flags = self.flags
        reqs = line[1]
        if reqs == []:
            return True
        else:
            for req in reqs:            
                if flags.check(*req) == False:
                    return False
                else:
                    return True

    def finalize(self):
        left = None
        right = None
        for line in self.left:
            if self.check(line) == True:
                left = line[0]
        for line in self.right:
            if self.check(line) == True:
                right = line[0]
        self.left = left
        self.right = right

class Title():
    def __init__(self, config):

        self.folder = config.RESOURCES
        self.screen = config.SCREEN
        self.size = config.SCREEN_SIZE
        self.find_position()
        self.text = None
        self.text_size = 16
        self.color = (201, 192, 187)

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
        font = pygame.font.Font(os.path.join(self.folder, "font", "advert.ttf"), self.text_size)  
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

class Cutscene():

    def __init__(self, data, flags):
        self.data = data
        self.flags = flags
        self.destination = None
        self.update()
    
    def update(self):
        if self.data is not None:
            self.format()
            self.finalize() 

    def format(self):
        from tools import req_format      
        data = self.data
        output = []
        for line in data:
            formatted_line = req_format(line)
            output.append(formatted_line)
        self.destination = output

    def check(self, line):
        flags = self.flags
        reqs = line[1]
        if reqs == []:
            return True
        else:
            for req in reqs:            
                if flags.check(*req) == False:
                    return False
                else:
                    return True

    def finalize(self):
        destination = None
        for line in self.destination:
            if self.check(line) == True:
                destination = line[0]
        self.destination = destination




