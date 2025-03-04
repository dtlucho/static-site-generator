import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me!</a>')

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("div", "Content", {"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), '<div class="container" id="main">Content</div>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode("", "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "value is required")

    def test_leaf_to_html_special_chars(self):
        node = LeafNode("p", "Text with <special> chars & symbols")
        self.assertEqual(node.to_html(), "<p>Text with <special> chars & symbols</p>")

    def test_leaf_to_html_different_tags(self):
        tags = ["h1", "h2", "h3", "span", "strong", "em"]
        for tag in tags:
            node = LeafNode(tag, f"Content in {tag}")
            self.assertEqual(node.to_html(), f"<{tag}>Content in {tag}</{tag}>")


if __name__ == "__main__":
    unittest.main() 