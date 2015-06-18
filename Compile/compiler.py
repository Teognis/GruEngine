class Compiler():

    def __init__(self):
        from compiler import Stream             
        self.default_folders()   


    def default_folders(self):
        import os
        from os import chdir
        from os.path import dirname
        OUTPUT = os.path.join(dirname(__file__), "output")
        INPUT = os.path.join(dirname(__file__), "input")
        self.output = OUTPUT
        self.input = INPUT


    def compile(self, folder=None):
        import os        
        from compiler import Stream           
        stream = Stream() 
        if folder:
            input_folder = folder
        else:
            input_folder = self.input_folder  
                
        fileSet = set() 
        for dir_, _, files in os.walk(input_folder):
            for fileName in files:
                relDir = os.path.relpath(dir_, input_folder)
                relFile = os.path.join(relDir, fileName)
                fileSet.add(relFile)
        
        for datafile in fileSet:
            if datafile.endswith(".yml"):
                filename = os.path.join(input_folder, datafile)
                stream_data = open(filename, "r")          
                stream.input(stream_data)

        return stream


    def dump(self, stream, output_folder):
        import yaml
        import os
        import io
        file_name = stream.metadata["title"]
        file_name = file_name + ".gru"
        full_path = os.path.join(output_folder, file_name)
        gru_file = open(full_path, "wb") 
        gru_file.seek(0)
        gru_file.truncate()        
        data = stream.__dict__
        # yaml.dump(data, gru_file, default_flow_style=False, allow_unicode=True, encoding=('utf-8'))
        # yaml.dump(data, gru_file, default_flow_style=False, encoding=('utf-8'))
        yaml.dump(data, gru_file, default_flow_style=False, encoding=('utf-8'))          
        gru_file.close()
        return full_path
        

    def decompile(self, file_path):
        import yaml
        from compiler import Stream 
        name = file_path       
        stream = Stream()
        stream_data = open(file_path, "r")
        data = yaml.load(stream_data)        
        for item in data.keys():
            key = str(item)
            data_type = data[key]
            # key = key.encode('utf-8')
            stream.input(data_type, key)  
        return stream   

                                        
                
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
        




