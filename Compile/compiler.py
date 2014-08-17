class Compiler():

    def __init__(self, file=None):
        from compiler import Stream           
        self.stream = Stream()         
        self.file = file
        self.find_folders()
        if file == None:
            self.compile()  
            self.dump(self.stream)             
        else:      
            self.decompile()               
            

    def find_folders(self):
        import os
        from os import chdir
        from os.path import dirname
        OUTPUT = os.path.join(dirname(__file__), "output")
        # INPUT = os.path.join(dirname(__file__), "input")
        INPUT = os.path.join(dirname(dirname(__file__)), "data")
        self.output_folder = OUTPUT
        self.input_folder = INPUT

    def compile(self):
        import os        
        input_folder = self.input_folder
        for datafile in os.listdir(input_folder):
            if datafile.endswith(".yml"):
                stream_data = open(os.path.join(input_folder, datafile), "r")                
                self.stream.input(stream_data)

    def dump(self, stream):
        import yaml
        import os
        file_name = stream.metadata["title"]
        file_name = file_name + ".gru"
        gru_file = open(os.path.join(self.output_folder, file_name), "wb")
        gru_file.seek(0)
        gru_file.truncate()        
        data = stream.__dict__
        yaml.dump(data, gru_file, default_flow_style=False)            
        gru_file.close()
        

    def decompile(self):
        import yaml
        gru_file = self.file
        stream = self.stream
        stream_data = open(gru_file, "r")
        data = yaml.load(stream_data)        
        for item in data.keys():
            key = str(item)
            data_type = data[key]          
            stream.input(data_type, key)     
        self.output = stream.output() 
        self.stream = stream
                                        
                
class Stream():

    def __init__(self):
        self.metadata = {}
        self.scenes = {}
        self.flags = {}
        self.combinations = {}
        self.items = {}
        self.clues = {}
        self.links = {}        


    def input(self, data, type = None):
        import yaml
        if type == None:
            data = yaml.load(data)
            key = data["gru_type"]
            del data["gru_type"]        
            self.__dict__[key].update(data)
        else:
            self.__dict__[type].update(data)

    def output(self):

        return self.scenes, self.links, self.flags, self.items, self.clues, self.combinations
        




