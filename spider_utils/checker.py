import sys

CONTAINER_MAP = {
    "root": ["p", "img", "table", "code", "h1", "h2", "h3", "h4", "h5", "video", "ol", "ul"],
    "p": ["a", "i", "b", "u", "strike", "_"],
    "table": ["tr"],
    "tr": ["td", "th"],
    "ol": ["li"],
    "a": ["_"],
    "i": ["_"],
    "b": ["_"],
    "u": ["_"],
    "strike": ["_"],
    "th": ["_"],
    "td": ["_"],
    "code": ["_"],
    "h1": ["_"],
    "h2": ["_"],
    "h3": ["_"],
    "h4": ["_"],
    "h5": ["_"],
    "li": ["_"],
    "img": [],
    "video": []
}

def containCheck(outter, inner):
    return (outter in CONTAINER_MAP) and (inner in CONTAINER_MAP[outter])

def attrCheck(attr, tagName):

    if tagName in ["img", "video"]:
        return attr in ["src"]
    if tagName in ["a"]:
        return attr in ["href"]
    else:
        return len(attr) == 0

def print_mark_str(v, mark=False):
    if mark:
        sys.stdout.write("\033[1;35m%s\033[0m" % v)
    else:
        sys.stdout.write("%s" % v)

class ResultNode:
    def __init__(self, tag, content=None, attrs={}) -> None:
        self.tag = tag
        self.__content = content
        self.attrs = attrs
        self.__children = []
        self.__marks = set()
        self.ok = True
    
    def _mark(self, v):
        self.__marks.add(v)
    
    def append_child(self, child):
        self.__children.append(child)
        self.ok = self.ok and child.ok

    def print(self, depth=0, indent=4):
        prefix_space = " " * (depth * indent)
        sys.stdout.write(prefix_space)
        if self.tag == "_":
            # Text Nodes
            print_mark_str("\"%s\"\n" % self.__content, "_" in self.__marks)
        elif self.tag == None:
            # Other Nodes
            print_mark_str("%s\n" % self.__content, "_" in self.__marks)
        else:
            # HTML Elements
            print_mark_str("<%s" % self.tag, "_" in self.__marks)
            for kw, value in self.attrs.items():
                print_mark_str(" %s=\"%s\"" % (kw, value), kw in self.__marks)

            if len(self.__children) > 0:
                print_mark_str(">\n", "_" in self.__marks)
            
                for child in self.__children:
                    child.print(depth + 1, indent)

                sys.stdout.write(prefix_space)
                print_mark_str("</%s>\n" % self.tag, "_" in self.__marks)
            else:
                print_mark_str(" />\n", "_" in self.__marks)

def treeCheck(node, context):
    from lxml import html

    ret = []

    for child in node:
        if isinstance(child, str):
            v = ResultNode("_", child)
            if not containCheck(context, "_"):
                v.ok = False
                v._mark("_")
            ret.append(v)
        elif isinstance(child, html.HtmlElement):
            v = ResultNode(child.tag, None, child.attrib)

            # contain check
            if not containCheck(context, child.tag):
                v.ok = False
                v._mark("_")

            # attr check
            for kw in v.attrs.keys():
                if not attrCheck(kw, v.tag):
                    v._mark(kw)
                    v.ok = False
            
            # children check
            for c in treeCheck( child.xpath("child::node()"), child.tag):
                v.append_child(c)
            ret.append(v)
        else:
            v = ResultNode(None, html.tostring(child, with_tail=False).decode("utf-8"))
            v.ok = False
            v._mark("_")
            ret.append(v)

    return ret
        
def checkHTML(doc):
    from lxml import html
    ret = ResultNode("root")
    try:
        for c in treeCheck( html.fragments_fromstring(doc), "root"):
            ret.append_child(c)
    except html.etree.ParseError:
        ret.ok = False
    return ret