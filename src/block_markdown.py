from enum import Enum
import re

from htmlnode import ParentNode
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
