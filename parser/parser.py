class Document:
    def __init__(self):
        self.content: list[Element] = []

    def __getattr__(self, name):
        for child in self.content:
            if child.name == name:
                return child
        raise AttributeError(name)


class Element:
    def __init__(self, name: str):
        self.name: str = name
        self.content: list[Element] = []
        self.value: object | None = None
        self.attribute: dict[str, str] = {}
        self.is_structure: bool = False

    def __getattr__(self, name: str):
        for child in self.content:
            if child.name == name:
                return child
        raise AttributeError(name)


def parse(source: str):
    pos = 0
    stack: list[Element] = []
    document = Document()
    while pos < len(source):
        if source[pos] == "<":
            pos += 1

            name = ""
            content = ""
            attributes: dict[str, str] = {}
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
                element.is_structure = True
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
                    content += source[pos]
                    pos+=1
                pos+=1
            elif source[pos]=='"' :#gestion des string ""
                pos+=1
                while source[pos]!='"':
                    content+=source[pos]
                    pos+=1
                pos+=1
            elif source[pos]=="'" :
                pos+=1
                while source[pos]!="'":
                    content+=source[pos]
                    pos+=1
                pos+=1
            else:
                while source[pos] != ";" and source[pos] !="<":
                    content += source[pos]
                    pos += 1
            match element.attribute.get("type"):
                case "string":
                    element.value = content
                case "float":
                    element.value = float(content)
                case _:
                    element.value = content

            if source[pos] == ";":
                pos += 1
            if stack:
                stack[-1].content.append(element)
            else:
                document.content.append(element)
        elif source[pos]=="}":
            pos+=1
            if source[pos]==";":
                pos+=1
                stack.pop()
        else:
            pos+=1
    return document
source='<doctype: web;><body:{<header type="string":{<h1 class="title": lorem ipsum;>};<main:{<p:§§;>};};'#test line
doc=parse(source)#test line
print(doc.body.header.h1.value)