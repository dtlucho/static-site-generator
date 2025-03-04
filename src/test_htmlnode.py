import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        children = [
            LeafNode("span", "first"),
            LeafNode("span", "second"),
            LeafNode("span", "third")
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><span>second</span><span>third</span></div>"
        )

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )

    def test_to_html_with_nested_parent_nodes(self):
        inner_child = LeafNode("span", "inner")
        middle_child = ParentNode("div", [inner_child])
        outer_child = ParentNode("section", [middle_child])
        parent_node = ParentNode("main", [outer_child])
        self.assertEqual(
            parent_node.to_html(),
            "<main><section><div><span>inner</span></div></section></main>"
        )

    def test_to_html_with_mixed_children(self):
        children = [
            LeafNode("span", "text"),
            ParentNode("div", [LeafNode("p", "paragraph")]),
            LeafNode("a", "link", {"href": "https://example.com"})
        ]
        parent_node = ParentNode("section", children)
        self.assertEqual(
            parent_node.to_html(),
            '<section><span>text</span><div><p>paragraph</p></div><a href="https://example.com">link</a></section>'
        )

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "tag is required")

    def test_to_html_with_empty_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "tag is required")

    def test_to_html_with_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "children is required")

    def test_to_html_with_complex_nesting(self):
        # Create a complex nested structure
        innermost = LeafNode("span", "innermost")
        inner = ParentNode("div", [innermost])
        middle = ParentNode("section", [inner])
        outer = ParentNode("main", [middle])
        self.assertEqual(
            outer.to_html(),
            "<main><section><div><span>innermost</span></div></section></main>"
        )

    def test_to_html_with_special_chars_in_children(self):
        children = [
            LeafNode("p", "Text with <special> chars"),
            LeafNode("p", "More text with & symbols")
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Text with <special> chars</p><p>More text with & symbols</p></div>"
        )


if __name__ == "__main__":
    unittest.main()
