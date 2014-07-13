
def glyph_links(text):              #creates Glyph markup out of Grue markup :)
    linklist = []
    tuples = []
    
    splittext = text.split(">")                 
    for i in splittext:
        indeks = i.find("<")
        if indeks is not -1:
            length = len(i)
            word = i[indeks+1:length]                    
            if word not in linklist:                     
                linklist.append(word)
    for i in linklist:
        tpl = i.split("/")
        tuples.append(tpl)
    
    for i in tuples:
        word = i[0]
        link = i[1]
        
        original = word + "/" + link
        oldstring = "<" + original + ">"
        newstring = "{link "+link+"; {"+link+"; "+word+"}}"          
        text = text.replace(oldstring, newstring)           
    return text


def split_reqs(text):
    output = []
    if "/" in text:
        list = []
        text = text.split("/")
        value = text[0].strip()
        reqs = text[1].strip()
    else:
        value = text
        reqs = []
    output = [value,reqs]
    
    return output

def list_reqs(text):
    output = []
    if " " in text:
        text = text.split()
        for i in text:                
            output.append(i)
    else:
        output.append(text)
    return output
    


def format_reqs(list):
    output = []          
    for req in list:        
        operators = ["=",">","<",">=","<="]
        for operator in operators:            
            if operator in req:
                req = req.split(operator)
                key = req[0].strip()
                operation = operator
                value = req[1].strip()                
                reqlist = [key,operation,value]
                output.append(reqlist)
    return output
                
        
def req_format(text):
    from tools import split_reqs, list_reqs, format_reqs
    text = split_reqs(text)
    text[1] = list_reqs(text[1])
    text[1] = format_reqs(text[1])
    return text

def list_effs(text):
    output = []
    if " " in text:
        text = text.split()
        for i in text:                
            output.append(i)
    else:
        output.append(text)
    return output

def format_effs(text):
    output = []          
    for eff in text:        
        operators = ["-=","+=","="]
        for operator in operators:            
            if operator in eff:
                eff = eff.split(operator)
                key = eff[0].strip()
                operation = operator
                value = eff[1].strip()                
                efflist = [key,operation,value]
                output.append(efflist)
    return output


def eff_format(text):
    from tools import list_effs, format_effs
    text = list_effs(text)
    output = format_effs(text)
    return output
