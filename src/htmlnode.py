class HtmlNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("to_html must be implemented by subclasses")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f'{k}="{v}"' for k, v in self.props.items()])


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")
        if self.tag is None or self.tag == "":
            return self.value
        props_html = self.props_to_html()
        props_html = f" {props_html}" if props_html else ""
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props: dict=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children is required")
        inner_html = "".join(child.to_html() for child in self.children)
        props_html = self.props_to_html()
        props_html = f" {props_html}" if props_html else ""
        return f"<{self.tag}{props_html}>{inner_html}</{self.tag}>"