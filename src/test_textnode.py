import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is also a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual("TextNode(This is a text node, italic, None)", repr(node))

    def test_repr2(self):
        node = TextNode("This is a text node", TextType.TEXT, "www.google.com")
        self.assertEqual(
            "TextNode(This is a text node, text, www.google.com)", repr(node)
        )

    def test_text_plain(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
