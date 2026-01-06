import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag="div", props=props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        props = {"class": "my-class"}
        children = [HTMLNode(tag="span", value="Hello")]
        node = HTMLNode(tag="div", value="Container", children=children, props=props)
        expected_repr = (
            "HTMLNode(tag=div, value=Container, children=[HTMLNode(tag=span, value=Hello, children=None, props=None)], "
            "props={'class': 'my-class'})"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_leaf_to_html_b_tag(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_img_with_props(self):
        node = LeafNode("img", " ", {"src": "test.jpg", "alt": "test"})
        result = node.to_html()
        self.assertIn('src="test.jpg"', result)
        self.assertIn('alt="test"', result)

    def test_leaf_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_empty_string_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

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


if __name__ == "__main__":
    unittest.main()
