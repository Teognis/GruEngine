class Wlink():

    def __init__(self, dict, flags):                       #creates an instance of a wheel link (which holds its name and both link paths)
        # print dict
        self.txt = ""
        self.left = ""
        self.right = ""
        self.link = ""
        self.flags = flags
        self.set_attributes(dict)       
        self.txt = self.collect(self.txt)        
        self.left = self.collect(self.left)
        self.right = self.collect(self.right)
        
        
    def set_attributes(self, dict):                 #generates attributes out of yml streeam
        for key, value in dict.items():
            key = key.lower()
            setattr(self,key,value)

    def collect_req(self, text):                    #creates a list of scalar requirements (which are designated with a "/" in Grue markup) from a string
        operator = "/"
        reqlist = []
        if operator in text:
            text = text.split(operator)
            reqs = text[1]
            reqs = reqs.split()
            for req in reqs:
                reqlist.append(req)        
        return reqlist

    def remove_req(self, text):
        if "/" in text:
            text = text.split("/")
            newtext = text[0]
            return newtext
        else:
            return text


    
    def interpret(self, text):                      #splits req "xyz=zyx" text into ["xyz", "zyx"]
        operators = ["=+","=-",">=","<=","="]        
        for operator in operators:
            if operator in text:
                splittext = text.split(operator)                
            else:
                splittext = text
        return splittext


    def check_flags(self, key, value):              #checks flag dictionary and returns 1 if the values are present
        flags = self.flags
        if self.flags.has_key(key):                  
            if self.flags[key] == int(value):                                      
                return 1
            else:
                return 0
        else:
            return 0
   
            
    def check_reqs(self, text):                     #main req_check function in Wlink
        reqlist = self.collect_req(text)
        if reqlist == []:
            return 1                        
        for req in reqlist:              
            keyval = self.interpret(req)
            if self.check_flags(*keyval) is not 1:
                return 0              
        return 1      
                              


    def collect(self, data):                           #collects text data from yml markup
        txt = data
        
        for i in txt[:]:
            name = txt.pop()            
            value = self.check_reqs(name)
            
            if value == 1:
                text = self.remove_req(name)
                return text
            if len(txt) == 0:                
                text = self.remove_req(name)
                return text

    
            

            
