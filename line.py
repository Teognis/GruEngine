class Line():
    def __init__(self, data):
        self.req = ""
        self.eff = ""
        self.set_attributes(data)
        self.collect_req()
        self.collect_eff()             
        
    def set_attributes(self, dict):
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_req(self):
        text = self.req
        text = text.split()
        req = []
        for i in text:
            req.append(i)
        self.req = req

    def collect_eff(self):
        text = self.eff
        text = text.split()
        eff = []
        for i in text:
            eff.append(i)
        self.eff = eff     
                       

    def interpret(self, text):
        operators = ["=+","=-",">=","<=","="]        
        for operator in operators:
            if operator in text:
                splittext = text.split(operator)                
            else:
                splittext = text
        return splittext
 

    def check_flags(self, list, flags):
        key = list[0]
        value = list[1]
        if flags.has_key(key):
            if flags[key] == value:
                return 1
        else:
            return 0        
      
    
    def check_req(self):
        reqs = self.req
        flags = {"house":3,"field":2}
        if reqs == []:
            return 1
        else:
            for req in reqs:
                newreq = self.interpret(req)
                value = self.check_flags(newreq, flags)
                if value == 0:
                    return 0
                else:
                    pass
            return 1
