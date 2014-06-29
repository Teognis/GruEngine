class State():
        
    import yaml        
    import os
    from os import chdir
    from os.path import dirname
    

    def __init__(self, scenedata, flagdata, wheel, title):

        from wheel import Wheel
        from scene import Scene
        import copy
        self.scenedata = copy.deepcopy(scenedata)       
        self.wheel = wheel
        self.title = title
        self.flagdata = flagdata              
        self.parents = []
        self.previous = None  
        self.scene = None 
                    
          

    def check_destination(self, destination):
        if self.scenedata.has_key(destination):           
            return destination
        else:
            return None

    def input(self, value, direction):        
                        
        if value == "Back":
            child = self.scene.title.lower()
            destination = self.find_parent(child)            

        elif value == "Continue":
            destination = self.scene.anchor.forward                    
        else:            
            wlink = self.scene.links[value]
            if direction == "left":
                destination = wlink.left
            elif direction == "right":
                destination = wlink.right        
            
        destination = self.check_destination(destination)
        if destination in self.scenedata:
            self.update(destination)
        else:
            print "Key not in scene dictionary!"
        
       
           
    def generate(self, name):
        from scene import Scene      
        flagdata = self.flagdata 
        scenedata = self.scenedata[name]
        scene = Scene(scenedata, flagdata) 
        scene.name = name              

        return scene
        
    def update(self, name):      
        from wheel import Wheel
        if self.scene is not None:        
            self.previous = self.scene.name                           
        scene = self.generate(name)                 
        self.scene = scene  
        if self.previous is not None:            
             self.set_parents()    
        self.output = self.scene.output
        title = self.scene.title
        self.title.update(title)     
        self.wheel.update(self.scene)  


    def set_parents(self):
        parent = self.previous        
        child = self.scene.name
        tpl = (child, parent)       
        if self.scene.anchor.type is not "Back":
            self.parents = []
        if self.scene.anchor.type == "Back":            
            self.parents.insert(0,tpl)
        else:
            pass
        

    def find_parent(self, child):
        for tpl in self.parents:
            if tpl[0] == child:
                parent = tpl[1]
                self.parents.remove(tpl)
                return parent
    
    def draw(self):
        self.wheel.draw()
        self.title.draw()

