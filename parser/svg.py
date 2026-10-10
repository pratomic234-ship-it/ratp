from parser import parse
from tkinter import *
source="<doctype:vector;><body:{<header:{<h1: lorem ipsum;>};<main:{<p:§§;>};};"
doc=parse(source)
if doc.doctype!="vector":
    print("type error")
    exit()
def parcourir(objet):
    for i in range(len(objet.content)):
        child=objet.content[i]
        parcourir(child)
        object_list=child
    return object_list
print(parcourir(doc))
class line:
    def __init__(self,doc):
        self.x1=doc.line.x1
        self.x2=doc.line.x2
        self.y1=doc.line.y1
        self.y2=doc.line.y2
        self.color=doc.line.color
    def render(self):
        print ()


print(doc.content)