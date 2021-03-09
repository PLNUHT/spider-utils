

def sanitize_attributes(doc):
    from lxml import html

    def clearTree(node):
        if isinstance(node, html.HtmlElement):
            if len(node.attrib) == 0:
                return
            keeps = []
            if node.tag in ["a"]:
                keeps.extend(["href"])
            elif node.tag in ["img", "video"]:
                keeps.extend(["src"])
            for it in node.attrib.keys():
                if it not in keeps:
                    del node.attrib[it]
            for c in node.xpath("child::node()"):
                clearTree(c)

    ret = []
    for it in html.fragments_fromstring(doc):
        clearTree(it)
        ret.append(html.tostring(it, encoding="unicode"))
    return "".join(ret)