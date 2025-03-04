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


if __name__ == "__main__":
    unittest.main()