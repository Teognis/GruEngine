class Flags():

    def __init__(self, flagdata):
        self.__flagdata__ = flagdata

    def generate(self, name):        
        from flags import Flag
        flags = self.__flagdata__
        if flags.has_key(name):
            data = flags[name]
        else:
            data = {}        
        flag = Flag(name,data)
        return flag

    def reset(self):
        flagdata = self.__flagdata__
        self.__dict__.clear()  
        self.__flagdata__ = flagdata   
  
    
    def set(self, key, operator, value):        
    
        model = self.generate(key)
        default = model.default
   
        if hasattr(self,key) == False:
            setattr(self, key, default)
      
        if hasattr(self,key) == True:
            old_value = getattr(self,key)

        if operator == "=":
            new_value = value
        elif operator == "+=":
            new_value = old_value + value
        elif operator == "-=":
            new_value = old_value - value  

        if int(new_value) > int(model.max):
            new_value = model.max
        if int(new_value) < int(model.min):
            new_value = model.min
           
        operator = "=" 
        value = int(new_value)        
        self.__dict__[key] = value
        

    def check(self, key, operator, value):
        value = int(value)
        
        if hasattr(self,key) == False:
            model = self.generate(key)
            default = model.default
            setattr(self, key, default)        

        if hasattr(self,key) == True:        
            if operator == "<":
                if getattr(self,key) < value:
                    return True
                else:
                    return False
            elif operator == "<=":
                if getattr(self,key) <= value:
                    return True
                else:
                    return False

            elif operator == "=":                
                if getattr(self,key) == value:                    
                    return True
                else:
                    return False
            elif operator == ">=":
                if getattr(self,key) >= value:
                    return True
                else:
                    return False
            elif operator == ">":
                if getattr(self,key) > value:
                    return True
                else:
                    return False

class Flag():

    def __init__(self, name, data):
        self.name = name
        self.set_default()
        self.min = 0
        self.max = 1
        self.set_attributes(data)

    def set_default(self):
        if self.name.startswith("lnk_"):
            default = 1
        else:
            default = 0
        self.default = default

    def set_attributes(self, dict):
        if dict is not None:
            for key, value in dict.items():
                key = key.lower()
                setattr(self,key,value)
