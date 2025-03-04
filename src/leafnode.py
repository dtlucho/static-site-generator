from htmlnode import HtmlNode

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
