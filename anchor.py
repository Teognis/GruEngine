class Anchor():
    def __init__(self, data, flags):   
        self.flags = flags
        self.forward = None
        self.type = None
        self.link = None     
        self.set_attributes(data)
        self.collect_link()

                           
    def set_attributes(self, dict):
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_link(self):
        
        if self.link is not None:                  
            
            self.forward = self.link[0]
        else:
            pass
