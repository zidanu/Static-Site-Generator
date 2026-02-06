import unittest

from splitnodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_no_delimiter_in_text(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

    def test_textnode_not_text_type_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

    def test_multiple_nodes_mixed_types(self):
        nodes = [
            TextNode("Start **bold** ", TextType.TEXT),
            TextNode("middle", TextType.BOLD),
            TextNode(" and **end**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("middle", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("end", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This **never closes", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_empty_segment_between_delimiters(self):
        node = TextNode("This is **** odd", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode(" odd", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delimiter_at_edges(self):
        node = TextNode("**bold at start** and **end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("bold at start", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("end", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://google.com) and another [second link](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just some plain text.", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_links_no_links(self):
        node = TextNode("Just some plain text.", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_split_images_non_text_node_untouched(self):
        node = TextNode("![img](url)", TextType.IMAGE, "url")
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_links_non_text_node_untouched(self):
        node = TextNode("[link](url)", TextType.LINK, "url")
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_split_images_single_image_only(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
            result,
        )

    def test_split_links_single_link_only(self):
        node = TextNode("[alt](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("alt", TextType.LINK, "https://example.com")],
            result,
        )

    def test_split_images_text_then_image(self):
        node = TextNode(
            "Look at this ![alt](https://example.com/img.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Look at this ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            ],
            result,
        )

    def test_split_images_image_then_text(self):
        node = TextNode(
            "![alt](https://example.com/img.png) is nice",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" is nice", TextType.TEXT),
            ],
            result,
        )

    def test_split_links_text_then_link(self):
        node = TextNode(
            "Click [here](https://example.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
            ],
            result,
        )

    def test_split_links_link_then_text(self):
        node = TextNode(
            "[here](https://example.com) is the site",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" is the site", TextType.TEXT),
            ],
            result,
        )

    def test_split_images_multiple_images(self):
        node = TextNode(
            "First ![one](https://ex.com/1.png) and ![two](https://ex.com/2.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://ex.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://ex.com/2.png"),
            ],
            result,
        )

    def test_split_links_multiple_links(self):
        node = TextNode(
            "Links: [one](https://ex.com/1) and [two](https://ex.com/2)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://ex.com/1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://ex.com/2"),
            ],
            result,
        )

    def test_split_pipeline_images_then_links(self):
        node = TextNode(
            "![logo](https://ex.com/logo.png) visit [site](https://ex.com)",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://ex.com/logo.png"),
                TextNode(" visit ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://ex.com"),
            ],
            nodes,
        )

    def test_split_links_does_not_treat_images_as_links(self):
        node = TextNode(
            "An image: ![alt](https://ex.com/img.png)",
            TextType.TEXT,
        )
        # First split images
        nodes = split_nodes_image([node])
        # Then split links
        nodes_after_links = split_nodes_link(nodes)

        self.assertListEqual(
            [
                TextNode("An image: ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://ex.com/img.png"),
            ],
            nodes_after_links,
        )

    def test_split_images_empty_alt(self):
        node = TextNode(
            "![](https://ex.com/img.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("", TextType.IMAGE, "https://ex.com/img.png")],
            result,
        )

    def test_split_links_empty_alt(self):
        node = TextNode(
            "[](https://ex.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("", TextType.LINK, "https://ex.com")],
            result,
        )

    def test_split_images_whitespace_around(self):
        node = TextNode(
            "  ![alt](https://ex.com/img.png)  ",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("  ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://ex.com/img.png"),
                TextNode("  ", TextType.TEXT),
            ],
            result,
        )

    def test_split_links_whitespace_around(self):
        node = TextNode(
            "  [alt](https://ex.com)  ",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("  ", TextType.TEXT),
                TextNode("alt", TextType.LINK, "https://ex.com"),
                TextNode("  ", TextType.TEXT),
            ],
            result,
        )

    def test_split_images_multiple_input_nodes(self):
        nodes = [
            TextNode("Before ![a](https://ex.com/a.png)", TextType.TEXT),
            TextNode("Middle", TextType.TEXT),
            TextNode("![b](https://ex.com/b.png) after", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://ex.com/a.png"),
                TextNode("Middle", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://ex.com/b.png"),
                TextNode(" after", TextType.TEXT),
            ],
            result,
        )

    def test_to_textnodes(self):
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://youtube.com"),
            ],
            text_to_textnodes(
                "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://youtube.com)"
            ),
        )
