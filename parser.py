class Document:
    def __init__(self):
        self.content = []
    def __getattr__(self, name):
        for child in self.content:
            if child.name == name:
                return child
class Element:
    def __init__(self):
        self.name=name
        self.content= []
    def __getattr__(self, name):
        for child in self.content:
            if child.name == name:
                return child.content
        raise AttributeError(name)
def parse(source):
    pos = 0
    stack = []
    root=[]
    document=Document()
    while pos < len(source):

        if source[pos] == "<":
            pos += 1

            name = ""

            while source[pos] != ":":#scan de l'id
                name += source[pos]
                pos += 1
            element=Element()
            pos += 1#pos placé après :
            if source[pos] == "{":
                pos += 1
                if stack:
                    stack[-1].content.append(element)
                else:
                    document.content.append(element)
                stack.append(element)
                continue
            content = ""
            while source[pos] != ";" and source[pos] !="<":
                content += source[pos]
                pos += 1
            element.content=content
            pos += 1
            if stack:
                stack[-1].content.append(element)
            else:
                document.content.append(element)
            print(element.name,"=",element.content)
        elif source[pos]=="}":
            pos+=1
            if source[pos]==";":
                pos+=1
                stack.pop()
        else:
            pos+=1
    
    