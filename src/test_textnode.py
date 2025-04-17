import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        node2 = TextNode("", TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_not_eq_empty_vs_nonempty(self):
        node = TextNode("", TextType.NORMAL)
        node2 = TextNode(" ", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_eq_image_type(self):
        node = TextNode("image.jpg", TextType.IMAGE, "https://example.com/image.jpg")
        node2 = TextNode("image.jpg", TextType.IMAGE, "https://example.com/image.jpg")
        self.assertEqual(node, node2)

    def test_eq_long_url(self):
        long_url = "https://example.com/very/long/path/with/many/segments/and/parameters?param1=value1&param2=value2"
        node = TextNode("Link text", TextType.LINK, long_url)
        node2 = TextNode("Link text", TextType.LINK, long_url)
        self.assertEqual(node, node2)

    def test_eq_special_chars(self):
        text = "Text with special chars: !@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
        node = TextNode(text, TextType.NORMAL)
        node2 = TextNode(text, TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        expected = "TextNode(This is a text node, BOLD, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_text_node_to_html_node_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "Alt text")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png"})

    def test_text_node_to_html_node_invalid_type(self):
        # Create a TextNode with an invalid type (this is a bit hacky for testing)
        invalid_type = "INVALID"
        node = TextNode("Test", invalid_type)
        with self.assertRaises(ValueError):
            TextNode.text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()