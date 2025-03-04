import unittest
from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode(
            "div",
            "Hello, world!",
            None,
            {"id": "greeting", "class": "text-center"}
        )
        self.assertEqual(node.props_to_html(), 'id="greeting" class="text-center"')

    def test_props_to_html_empty(self):
        node = HtmlNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HtmlNode("div", "Hello, world!", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HtmlNode(
            "div",
            "Hello, world!",
            [HtmlNode("p", "Child text")],
            {"id": "greeting"}
        )
        expected = "HtmlNode(div, Hello, world!, [HtmlNode(p, Child text, None, None)], {'id': 'greeting'})"
        self.assertEqual(repr(node), expected)

    def test_repr_empty(self):
        node = HtmlNode()
        expected = "HtmlNode(None, None, None, None)"
        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HtmlNode("div", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_constructor_with_all_params(self):
        node = HtmlNode(
            "div",
            "Hello, world!",
            [HtmlNode("p", "Child text")],
            {"id": "greeting"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props, {"id": "greeting"})

    def test_constructor_with_minimal_params(self):
        node = HtmlNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_constructor_with_some_params(self):
        node = HtmlNode("p", "Simple text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Simple text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()
