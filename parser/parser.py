class Document:
    def __init__(self):
        self.content = []
    def __getattr__(self, name):
        for child in self.content:
            if child.name == name:
                return child.content
class Element:
    def __init__(self,name):
        self.name=name
        self.content= []
        self.attribute={}
    def __getattr__(self, name):
        for child in self.content:
            if child.name == name:
                return child.content
        raise AttributeError(name)
def parse(source: str):
    pos = 0
    stack = []
    root=[]
    document=Document()
    while pos < len(source):
        if source[pos] == "<":
            pos += 1

            name = ""
            content = ""
            attributes={}
            # Lire le nom jusqu'à l'espace qui annonce un attribut, ou jusqu'à :
            while source[pos] != " " and source[pos] != ":":
                name += source[pos]
                pos += 1
            # Lire les attributs jusqu'au :
            while source[pos] != ":":
                if source[pos] == " ":
                    pos += 1
                    continue
                attribute_name = ""
                while source[pos] != "=":
                    attribute_name += source[pos]
                    pos += 1
            
                pos += 1  # passer le =
                pos += 1  # passer le guillemet ouvrant
                attribute_content = ""
                while source[pos] != '"':
                    attribute_content += source[pos]
                    pos += 1
                pos += 1  # passer le guillemet fermant
                attributes[attribute_name] = attribute_content
            element=Element(name)
            element.attribute=attributes
            pos += 1#pos placé après :
            if source[pos] == "{":#verification d'une structure
                pos += 1
                if stack:
                    stack[-1].content.append(element)
                else:
                    document.content.append(element)
                stack.append(element)
                continue
            elif source[pos]=="§":
                pos+=1
                while source[pos]!="§":
                    if source[pos]!="<":
                        content=content+source[pos]
                        if source[pos]==";":
                            element.content.append(content)
                            pass
                    else:
                        while source[pos]!=":":
                            pos+=1
                        pos+=1
                        while source[pos]!=";":
                            content=content+source[pos]
                            pos+=1
                        pos+=1
                        while source[pos]!=">":
                            pos+=1
                        pos+=1
                        if source[pos]==";":
                            element.content.append(content)
                            pass
                        continue
                    pos+=1
                pos+=1
            elif source[pos]=='"' :#gestion des string ""
                pos+=1
                while source[pos]!='"':
                    content+=source[pos]
                    pos+=1
                continue
            elif source[pos]=="'" :
                pos+=1
                while source[pos]!="'":
                    content+=source[pos]
                    pos+=1
            while source[pos] != ";" and source[pos] !="<":
                content += source[pos]
                pos += 1
            element.content.append(content)
            pos += 1
            if stack:
                stack[-1].content.append(element)
            else:
                document.content.append(element)
            print(element.name,"=",element.content)#test line. remove
        elif source[pos]=="}":
            pos+=1
            if source[pos]==";":
                pos+=1
                stack.pop()
        else:
            pos+=1
    return document
source="<doctype: web;><body:{<header:{<h1: lorem ipsum;>};<main:{<p:§§;>};};"#test line
parse(source)#test line