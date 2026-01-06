from textnode import TextNode, TextType
from markdown_extract import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Unmatched delimiter in text")
        
        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_node = TextNode(part, TextType.TEXT)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(part, text_type)
                new_nodes.append(new_node)
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for link_text, link_url in links:
            markdown = f"[{link_text}]({link_url})"
            before, text = text.split(markdown, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for image_alt, image_url in images:
            markdown = f"![{image_alt}]({image_url})"
            before, text = text.split(markdown, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes
