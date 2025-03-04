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
