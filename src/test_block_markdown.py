import unittest
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines_lines(self):
        md = """



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_empty_lines_with_text(self):
        md = """This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_error(self):
        block = "####### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\npython\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = ">This is a quote\n>This is the same quote on a new line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list\n- with items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a list\n2. with items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_paragraphs(self):
        md = """
# This is a heading

## This is a subheading

### This is a **subsubheading**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a subheading</h2><h3>This is a <b>subsubheading</b></h3></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> This is the same quote on a new line
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nThis is the same quote on a new line</blockquote></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> This is the same quote on a new line
> This is a **bolded** quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nThis is the same quote on a new line\nThis is a <b>bolded</b> quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li></ul></div>",
        )

    def unordered_list_with_formatted_text(self):
        md = """
- This is a list
- with items
- This is a **bolded** list
- This is a _italic_ list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>This is a <b>bolded</b> list</li><li>This is a <i>italic</i> list</li></ul></div>",
        )   

    def ordered_list(self):
        md = """
1. This is a list
2. with items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li></ol></div>",
        )

    def ordered_list_with_formatted_text(self):
        md = """
1. This is a list
2. with items
3. This is a **bolded** list
4. This is a _italic_ list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li><li>This is a <b>bolded</b> list</li><li>This is a <i>italic</i> list</li></ol></div>",
        )

    def paragraph(self):
        md = """
This is a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph</p></div>",
        )

    def paragraph_with_formatted_text(self):
        md = """
This is a **bolded** paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()   
        self.assertEqual(
            html,
            "<div><p>This is a <b>bolded</b> paragraph</p></div>",
        )


if __name__ == "__main__":
    unittest.main()