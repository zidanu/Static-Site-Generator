import unittest

from mdextraction import extract_markdown_images, extract_markdown_links


class TestMDExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual(
            [
                ("to google", "https://www.google.com"),
                ("to youtube", "https://www.youtube.com"),
            ],
            matches,
        )

    def test_single_image(self):
        text = "Look at this ![alt text](https://example.com/img.png)"
        self.assertEqual(
            [("alt text", "https://example.com/img.png")],
            extract_markdown_images(text),
        )

    def test_single_link(self):
        text = "Go [here](https://example.com) now"
        self.assertEqual(
            [("here", "https://example.com")],
            extract_markdown_links(text),
        )

    def test_multiple_images(self):
        text = "First ![one](url1) and ![two](url2)"
        self.assertEqual(
            [("one", "url1"), ("two", "url2")],
            extract_markdown_images(text),
        )

    def test_multiple_links(self):
        text = "Links: [a](u1) and [b](u2) and [c](u3)"
        self.assertEqual(
            [("a", "u1"), ("b", "u2"), ("c", "u3")],
            extract_markdown_links(text),
        )

    def test_images_do_not_capture_links(self):
        text = "![img](img.png) and [link](page.html)"
        self.assertEqual(
            [("img", "img.png")],
            extract_markdown_images(text),
        )

    def test_links_do_not_capture_images(self):
        text = "![img](img.png) and [link](page.html)"
        self.assertEqual(
            [("link", "page.html")],
            extract_markdown_links(text),
        )

    def test_no_images(self):
        text = "Nothing to see here, just text and [a link](url)"
        self.assertEqual([], extract_markdown_images(text))

    def test_no_links(self):
        text = "Only ![an image](url.png) here"
        self.assertEqual([], extract_markdown_links(text))

    def test_empty_string(self):
        self.assertEqual([], extract_markdown_images(""))
        self.assertEqual([], extract_markdown_links(""))

    def test_leading_trailing_whitespace(self):
        text = "  Text ![img](url.png)  "
        self.assertEqual(
            [("img", "url.png")],
            extract_markdown_images(text),
        )

    def test_alt_text_with_spaces(self):
        text = "![a nice image](url.png)"
        self.assertEqual(
            [("a nice image", "url.png")],
            extract_markdown_images(text),
        )

    def test_link_text_with_spaces(self):
        text = "Click [this cool link](url)"
        self.assertEqual(
            [("this cool link", "url")],
            extract_markdown_links(text),
        )

    def test_link_lookalike_not_image(self):
        text = "I typed this: ![not really](just text)"
        # should still match as image; this ensures the image regex works
        self.assertEqual(
            [("not really", "just text")],
            extract_markdown_images(text),
        )

    def test_negative_lookbehind_for_links(self):
        text = "![image](img.png) and [link](page.html)"
        self.assertEqual(
            [("link", "page.html")],
            extract_markdown_links(text),
        )

    def test_mixed_multiline(self):
        text = """
        Intro text
        ![logo](logo.png)

        Visit [home](https://example.com) or
        check ![diagram](diag.svg) then [docs](https://example.com/docs)
        """
        self.assertEqual(
            [("logo", "logo.png"), ("diagram", "diag.svg")],
            extract_markdown_images(text),
        )
        self.assertEqual(
            [("home", "https://example.com"), ("docs", "https://example.com/docs")],
            extract_markdown_links(text),
        )
