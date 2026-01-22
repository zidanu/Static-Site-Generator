import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        self.assertEqual(' href="https://www.google.com"', node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode(
            "a",
            "link",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_html_exception(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "some text", None, None)
        self.assertEqual(
            "(tag=p, value=some text, children=None, props=None)", repr(node)
        )

    def test_repr2(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        self.assertEqual(
            "(tag=a, value=link, children=None, props={'href': 'https://www.google.com'})",
            repr(node),
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual("<p>Hello, world!</p>", node.to_html())

    def test_leaf_to_html_exception(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_p3(self):
        node = LeafNode(None, "nothing")
        self.assertEqual("nothing", node.to_html())

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("span", "hi", {"class": "greeting", "id": "main"})
        html = node.to_html()
        self.assertIn("<span ", html)
        self.assertIn('class="greeting"', html)
        self.assertIn('id="main"', html)
        self.assertIn(">hi</span>", html)

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            "(tag=a, value=Click me!, props={'href': 'https://www.google.com'})",
            repr(node),
        )

    def test_repr2(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual("(tag=p, value=Hello, world!, props=None)", repr(node))


class TestParentNode(unittest.TestCase):
    def test_to_html_tag_exception(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_child_exception(self):
        node = ParentNode("div", None)
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

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        LeafNode(
                            "h1", "Welcome", {"class": "title", "id": "main-title"}
                        ),
                        LeafNode(
                            "p",
                            "Some intro text.",
                            {"class": "body-text", "data-theme": "dark"},
                        ),
                    ],
                    {"class": "container", "data-role": "page-section"},
                ),
                LeafNode(
                    "footer",
                    "Footer content",
                    {"class": "site-footer", "style": "color: gray;"},
                ),
            ],
            {"id": "root", "lang": "en"},
        )
        self.assertEqual(
            node.to_html(),
            '<div id="root" lang="en"><section class="container" data-role="page-section"><h1 class="title" id="main-title">Welcome</h1><p class="body-text" data-theme="dark">Some intro text.</p></section><footer class="site-footer" style="color: gray;">Footer content</footer></div>',
        )


if __name__ == "__main__":
    unittest.main()
