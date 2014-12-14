class State():
        
    import yaml        
    import os
    from os import chdir
    from os.path import dirname
    

    def __init__(self, stream, flags, inventory, wheel, combiner, title, page):

        from wheel import Wheel
        from scene import Scene
        import copy

        self.scenedata = copy.deepcopy(stream.scenes)
        self.linkdata = copy.deepcopy(stream.links)
        self.inventory = inventory
        self.flags= flags
        self.combiner = combiner
        
        self.wheel = wheel
        self.title = title                   
        self.parents = []
        self.page = page
        self.previous = None  
        self.scene = None 
        self.snapshot = None 
        self.links = [] 
        self.raw = ""                 

    def generate(self, name):
        from scene import Scene           
        scene = Scene(name, self.scenedata[name], self.flags) 
        scene.name = name          
        return scene

    def save(self, scene):
        filedict = {}
        flags = {}
        previous = None
        if self.scene is not None:        
            previous = self.scene.name 
        for key, value in self.flags.__dict__.items():
            flags[key] = value      
        filedict["flags"] = flags
        filedict["scene"] = scene
        filedict["previous"] = previous
        self.snapshot = filedict      

    def reset(self):
        self.flags.reset()
        self.previous = None
        self.scene = None
        

    def restore(self, filedict):
        self.reset()
        self.previous = filedict["previous"]
        flags = filedict["flags"]
        for key, value in flags.items():
            setattr(self.flags, key, value)
        scene = filedict["scene"]
        self.update(scene)

        
    def update(self, name):      
        from wheel import Wheel
        if self.scene is not None:        
            self.previous = self.scene.name
        self.save(name)                           
        scene = self.generate(name) 
        cutscene = scene.cutscenes.destination
        if cutscene is not None:
            self.follow(cutscene)
        else:              
            self.scene = scene 

            if self.previous is not None:        
                 self.set_parents()  
            self.output = self.scene.output
            self.raw = self.scene.raw
            title = self.scene.title
            self.inventory.update()
            self.title.update(self.scene.title)     
            self.wheel.update(self.scene)
            self.links = self.scene.hyperlinks
            self.page.update(self.output, self.links, self.raw)
 

    def input(self, input_id, input_type, direction, button):                 
        if input_type == "lnk":
            input_id = self.check_link(input_id)  
        if input_type == "mnu" and button == "up":  
            self.menu.input(input_id)    
        self.combiner.input(input_id)

        if len(self.combiner.box) == 2:
            destination, found_combination, warning = self.combiner.check()
            if found_combination == None:
                self.scene_input(input_id, input_type, direction)  
            elif found_combination == 1:
                self.follow(destination)
            elif found_combination == 0:
                print warning

    def check_link(self, link):
        from tools import check_flags        
        if self.flags.check( link, "=" , 1 ):                
            return link
        else:
            link = link.replace("lnk_","hdn_")
            return link

    def scene_input(self, input_id, input_type, direction):
        from scene import Link
        if input_type == "whl":
            input_id = input_id.strip("whl_")            
            if input_id == "Back":
                child = self.scene.name
                destination = self.find_parent(child)          
            elif input_id == "Continue":
                destination = self.scene.anchor.forward                    
            else:          
                input_id = int(input_id)  
                wlink = self.scene.links[input_id]
                if direction == "left":
                    destination = wlink.left               
                elif direction == "right":
                    destination = wlink.right
            self.follow(destination)  
        elif input_type == "lnk": 
            if self.linkdata.has_key(input_id):        
                link = Link(input_id,self.linkdata,self.flags)
                if direction == "left":
                    destination = link.left
                    self.follow(destination)
                elif direction == "right":
                    destination = link.right
                    self.follow(destination)
            else:
                if input_id.startswith("hdn_"):
                    link = input_id.replace("hdn_","lnk_")
                    print "Link *" + str(link) + "* is hidden and cannot be interacted with!"
                else:
                    print "Key *" + str(input_id) + "* not in link dictionary!"
        elif input_type == "inv":         
            instance = None
            for item in self.inventory.pool:
                if item.id == input_id:
                    instance = item
            if direction == "left":
                destination = instance.left
                self.follow(destination)
            elif direction == "right":
                destination = instance.right
                self.follow(destination)
        else:
            pass        


    def check_destination(self, destination):
        if self.scenedata.has_key(destination):           
            return destination
        else:
            return None             
           
        
    def follow(self, destination):
        original_destination = destination
        destination = self.check_destination(destination)
        if destination in self.scenedata:
            self.update(destination)
        else:
            print "Key " + str(original_destination) + " not in scene dictionary!" 

    def set_parents(self):
        parent = self.previous        
        child = self.scene.name
        tpl = (child, parent)  
        if self.scene.anchor == None:
            self.parents = []
        else:
            if self.scene.anchor.type == "Continue":
                self.parents = []
            if self.scene.anchor.type == "Back":     
                self.parents.append(tpl)      

    def find_parent(self, child):
        for tpl in self.parents:
            if tpl[0] == child:
                parent = tpl[1]
                self.parents.remove(tpl)
                return parent
    
        

