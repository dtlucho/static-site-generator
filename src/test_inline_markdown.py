import unittest
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    # Basic functionality tests
    def test_basic_delimiter(self):
        # Test with a single delimiter pair
        node = TextNode('This is a `code` text', TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        
    def test_multiple_delimiters(self):
        # Test with multiple delimiter pairs
        node = TextNode('This is a `code` text and `code2` text', TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text and ")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        self.assertEqual(result[3].text, "code2")
        self.assertEqual(result[3].text_type, TextType.CODE)
        self.assertEqual(result[4].text, " text")
        self.assertEqual(result[4].text_type, TextType.NORMAL)
        
    def test_different_delimiter_types(self):
        # Test with different delimiter types
        node = TextNode('This is a _italic_ text and `code` text', TextType.NORMAL)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text and `code` text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        
    def test_multi_character_delimiter(self):
        # Test with multi-character delimiters
        node = TextNode('This is a **bold** text', TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
    
    # Edge cases
    def test_empty_text(self):
        # Test with empty text
        node = TextNode('', TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
        
    def test_no_delimiters(self):
        # Test with text that has no delimiters
        node = TextNode('This is a normal text', TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a normal text")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        
    def test_delimiter_at_beginning(self):
        # Test with delimiter at the beginning
        node = TextNode('`code` is a normal text', TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "code")
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, " is a normal text")
        self.assertEqual(result[1].text_type, TextType.NORMAL)
        
    def test_delimiter_at_end(self):
        # Test with delimiter at the end
        node = TextNode('This is a normal text `code`', TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is a normal text ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        
    def test_multiple_input_nodes(self):
        # Test with multiple nodes in the input list
        node1 = TextNode('This is a normal text', TextType.NORMAL)
        node2 = TextNode('`code` is a normal text', TextType.NORMAL)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a normal text")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " is a normal text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        
        
        
    def test_non_text_nodes(self):
        # Test with non-TEXT type nodes
        node = TextNode('This is a normal text', TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a normal text")
        self.assertEqual(result[0].text_type, TextType.BOLD)
    
    # Error cases
    def test_missing_closing_delimiter(self):
        # Test with missing closing delimiter
        node = TextNode('This is a `code text', TextType.NORMAL)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "No closing delimiter ` found in text 'This is a `code text'")

        
    def test_invalid_delimiter(self):
        # Test with invalid delimiter
        node = TextNode('This is a <code> text', TextType.NORMAL)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "<", TextType.CODE)
        self.assertEqual(str(context.exception), "No closing delimiter < found in text 'This is a <code> text'")

    def test_extract_markdown_images(self):
        text = "This is a ![image](https://example.com/image.png) text"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('image', 'https://example.com/image.png')])

    def test_extract_markdown_images_no_images(self):
        text = "This is a text"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_multiple_markdown_images(self):
        text = "This is a ![image](https://example.com/image.png) text and ![image2](https://example.com/image2.png) text"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('image', 'https://example.com/image.png'), ('image2', 'https://example.com/image2.png')])

    def test_extract_markdown_links(self):
        text = "This is a [link](https://example.com) text"
        result = extract_markdown_links(text)
        self.assertEqual(result, [('link', 'https://example.com')])

    def test_extract_markdown_links_no_links(self):
        text = "This is a text"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_multiple_markdown_links(self):
        text = "This is a [link](https://example.com) text and [link2](https://example.com/link2) text"
        result = extract_markdown_links(text)
        self.assertEqual(result, [('link', 'https://example.com'), ('link2', 'https://example.com/link2')])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            result,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

if __name__ == "__main__":
    unittest.main()