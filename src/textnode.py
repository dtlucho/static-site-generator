from enum import Enum
from htmlnode import LeafNode

TextType = Enum("TextType", ["NORMAL", "BOLD", "ITALIC", "LINK", "IMAGE"])

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
    
    def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.NORMAL:
                return LeafNode("p", text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", text_node.text, {"src": text_node.url})
            case _:
                raise ValueError(f"Invalid text type: {text_node.text_type}")
    
    