class State():
        
    import yaml        
    import os
    from os import chdir
    from os.path import dirname
    

    def __init__(self, scenedata, linkdata, flags, inventory, wheel, combiner, title):

        from wheel import Wheel
        from scene import Scene
        import copy

        self.scenedata = copy.deepcopy(scenedata)
        self.linkdata = copy.deepcopy(linkdata)
        self.inventory = inventory
        self.combiner = combiner
        self.flags= flags
        self.wheel = wheel
        self.title = title                   
        self.parents = []
        self.previous = None  
        self.scene = None 
        self.snapshot = None                    

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
        # for key, value in dict.items():
        #         key = key.lower()
        #         setattr(self,key,value)

        
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
            title = self.scene.title
            self.inventory.update()
            self.title.update(self.scene.title)     
            self.wheel.update(self.scene)
 

    def input(self, l_click, w_click, i_click, direction, button):      
        input_id, input_type = self.determine_input(l_click, w_click, i_click)

        if input_id is not None and input_type is not "whl":
            if input_type is "lnk": 
                if self.check_link(input_id):                                                          
                    self.combiner.input(input_id)
            else:
                self.combiner.input(input_id)

        if button == "up":
            destination, found_combination, warning = self.combiner.check()
            if found_combination == None:
                self.scene_input(input_id, input_type, direction)  
            elif found_combination == 1:
                self.follow(destination)
            elif found_combination == 0:
                print warning

    def check_link(self, link):
        from tools import check_flags
        if len(self.combiner.box) == 0:
            if self.flags.check( link, "=" , 1 ):
                return True
        elif len(self.combiner.box) == 1:
            item_id = self.combiner.box[0]            
            for entity in self.inventory.pool:
                if entity.id == item_id:
                    item = entity
                    for revealed_link in item.reveal:
                        if revealed_link[0] == link:
                            if check_flags(revealed_link, self.flags):
                                return True
        else:
            return False


    def scene_input(self, input_id, input_type, direction):
        from scene import Link
        if input_type == "whl":
            if input_id == "Back":
                child = self.scene.name
                destination = self.find_parent(child)          
            elif input_id == "Continue":
                destination = self.scene.anchor.forward                    
            else:            
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
                print "Key " + str(input_id) + " not in link dictionary!"
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
        

    def determine_input(self, l_click, w_click, i_click):
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
            
        return input_id, input_type


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
        if self.scene.anchor.type != "Back":
            self.parents = []
        if self.scene.anchor.type == "Back":     
            self.parents.append(tpl)      

    def find_parent(self, child):
        for tpl in self.parents:
            if tpl[0] == child:
                parent = tpl[1]
                self.parents.remove(tpl)
                return parent
    
    def draw(self):
        self.wheel.draw()
        self.title.draw()
        self.inventory.draw()
        

