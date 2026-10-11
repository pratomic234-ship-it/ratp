from parser.parser import parse
from tkinter import *#type:ignore
source="<doctype:vector; <line:{<x1:155;<y1:100;<x2:175;<y2:100;<color:#FFD700;};"
doc=parse(source)
if doc.doctype!="vector":
    print("the document is ")
    raise(TypeError)
    
def parcourir(objet):
    for i in range(len(objet.content)):
        child=objet.content[i]
        parcourir(child)
        object_list+=child
    return object_list
for i in parcourir(doc):
    match i:
        case "line":
            ""
        case "circle":
            ""
print(parcourir(doc))
class line:
    def __init__(self,doc):
        self.x1=doc.line.x1
        self.x2=doc.line.x2
        self.y1=doc.line.y1
        self.y2=doc.line.y2
        self.color=doc.line.color
    def render(self):
        print()


print(doc.content)