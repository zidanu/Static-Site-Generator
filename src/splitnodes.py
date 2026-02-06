import re
from textnode import TextNode, TextType
from mdextraction import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Markdown syntax error: missing closing delimiter")

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes


def split_nodes_helper(old_nodes, pattern, text_type, extract):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = re.split(rf"({pattern})", node.text)

        for part in parts:
            if part == "":
                continue
            if re.fullmatch(pattern, part) and len(links := extract(part)) == 1:
                ((text, link),) = links
                new_nodes.append(TextNode(text, text_type, link))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_helper(
        old_nodes, r"!\[[^\]]*]\([^)]*\)", TextType.IMAGE, extract_markdown_images
    )


def split_nodes_link(old_nodes):
    return split_nodes_helper(
        old_nodes, r"(?<!!)\[[^\]]*]\([^)]*\)", TextType.LINK, extract_markdown_links
    )


def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
