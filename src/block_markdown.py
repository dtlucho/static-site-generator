from enum import Enum
import re

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    blocks = []
    for s in splitted:
        if s.strip() == "":
            continue
        blocks.append(s.strip())
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.ULIST

    if block.startswith("1. "):
        if all(re.match(r"^\d+\. ", line) for line in lines):
            numbers = [int(line.split(".")[0]) for line in lines]
            if all(numbers[i] == numbers[i-1] + 1 for i in range(1, len(numbers))):
                return BlockType.OLIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.ULIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.OLIST:
                children.append(ordered_list_to_html_node(block))
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
    
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [TextNode.text_node_to_html_node(c) for c in text_nodes]

def heading_to_html_node(block):
    lines = block.split(" ")
    level = len(lines[0])
    text = " ".join(lines[1:])
    children = text_to_children(text)
    return ParentNode("h" + str(level), children)

def code_to_html_node(block):
    lines = block.split("\n")
    code = "\n".join(lines[1:-1])   
    return ParentNode("pre", [LeafNode("code", code + "\n")])

def quote_to_html_node(block):
    lines = block.split("\n")
    content = [line[2:] for line in lines]
    text = " ".join(content)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_content = line[2:]
        line_children = text_to_children(line_content)
        children.append(ParentNode("li", line_children))
    return ParentNode("ul", children)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_content = re.sub(r"^\d+\. ", "", line)
        line_children = text_to_children(line_content)
        children.append(ParentNode("li", line_children))
    return ParentNode("ol", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)