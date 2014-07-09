class Combiner():

    def __init__(self, data, flags):
        import copy
        self.data = copy.deepcopy(data)
        self.combinations = {}
        self.flags = flags
        self.populate()
        self.box = []

    def generate(self, name):
        from combiner import Combination
        data = self.data[name]
        combination = Combination(name, data, self.flags)
        key = combination.key
        self.combinations[key] = combination

    def populate(self):
        for combination in self.data:
            self.generate(combination)

    def input(self, item):   
        
        if len(self.box) < 2:
            self.box.append(item)  
       
    def check(self):
        destination = None
        found_combination = None
        warning = None
        if len(self.box) == 1:
            destination = self.box[0]
            self.box = []
            # warning = "Only one item in combiner box!"
        if len(self.box) == 2:
            if self.box[0] == self.box[1]:
                destination = self.box[0]
                self.box = []
                # warning = "Items in combiner box are one and the same"
            else:
                destination, found_combination, warning = self.find_combination()
                self.box = []

        return destination, found_combination, warning
      
    def find_combination(self):
        key = tuple(self.box)
        destination = None
        found_combination = 0
        warning = None

        if self.combinations.has_key(key):            
            combination = self.combinations[key]
            combination.update()
            found_combination = 1
            destination = combination.destination
            # warning = "Combination found!"
        else:
            item1 = str(key[0])
            item2 = str(key[1])
            warning = "Combination of " + item1 + " and " + item2 + " wasn't found in yml data!"

        return destination, found_combination, warning
                
        
class Combination():

    def __init__(self, name, data, flags):
        import copy
        self.name = name
        self.generate_key()
        self.data = data
        self.flags = flags

    def generate_key(self):
        name = self.name
        split_string = name.split("+")
        key_list = []
        for item in split_string:
            item = item.strip()
            key_list.append(item)
        key_list.sort()
        key = tuple(key_list)
        self.key = key

    def format(self):
        from tools import req_format
        data = self.data
        destination = []
        for line in data:
            formatted_line = req_format(line)
            destination.append(formatted_line)
        self.destination = destination


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
        for line in self.destination:
            if self.check(line) == True:
                data = line[0]
        self.destination = data

    def update(self):
        self.destination = None
        self.format()
        self.finalize()
        
