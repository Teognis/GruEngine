

class Scene():


    

    def __init__(self, data, flags):
        import copy        
        
        self.data = copy.deepcopy(data)        
        self.flags = flags
        self.links = {}
        self.macros = {}
        self.segments = []
        self.variations = []      
        self.set_attributes(self.data)                      
        self.collect_segments()
        self.collect_variations()               
        self.collect_wheel()
        self.collect_anchor()
        self.create_output()
     
        
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
        from line import Line        
        segments = self.segments
        segpool = []
        for segment in segments:
            varpool = []
            for variation in segment:
                var = Line(variation)
                varpool.append(var)
            segpool.append(varpool)
        self.pool = segpool

    def collect_anchor(self):             #je samega sebe!!!!
        from anchor import Anchor        
        self.anchor = Anchor(self.anchor, self.flags)
                

    def create_output(self):

        def update_macro(list, word):               #updates the color dictionary for Glyph links (each link gets its own colour - prohack.com)
            list[word] = ("color", (135,13,145))


        def glyph_links(text):              #creates Glyph markup out of Grue markup :)
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
    
            for i in tuples:
                word = i[0]
                link = i[1]
                self.macros[link] = ("color", (135,13,145))                

                original = word + "/" + link
                oldstring = "<" + original + ">"
                newstring = "{link "+link+"; {"+link+"; "+word+"}}"          
                text = text.replace(oldstring, newstring)            
            return text
        
        output = ""
        pool = self.pool
        for segment in pool:
            for variation in segment:
                output = output + variation.txt
        output = glyph_links(output)        
        self.output = output
    
    
    
    def collect_wheel(self):
        from wlink import Wlink
         
        def create_wlinks(data):
            from wlink import Wlink
            wheeldata = {}
            items = data.items()
            for key, value in items:
           
                wlink = Wlink(value, self.flags)
                wheeldata[key] = wlink
            return wheeldata       
        wlinks = create_wlinks(self.wheel)
        
        self.links.update(wlinks)
        

        
        
        
        
        
        

