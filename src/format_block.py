from htmlnode import ParentNode
from format_markdown import text_to_text_nodes
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    block_list = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        else:
            block_list.append(section.strip())
    return block_list


def block_to_block_type(markdown_block):
    block_lines = markdown_block.split("\n")
    # Detecting a heading
    for i in range(len(markdown_block) - 1):
        if markdown_block[i] == "#":
            continue
        elif markdown_block[i] == " " and markdown_block[i - 1] == "#" and i < 7:
            return "heading"
        else:
            break

    # Detecting code blocks
    end = len(markdown_block) - 1
    if (
        markdown_block[0] == "`"
        and markdown_block[1] == "`"
        and markdown_block[2] == "`"
    ):
        if (
            markdown_block[end] == "`"
            and markdown_block[end - 1] == "`"
            and markdown_block[end - 2] == "`"
        ):
            return "code"

    # Detecting quote block
    if markdown_block[0] == ">":
        return "quote"

    # Detecting unordered list
    for line in block_lines:
        if (line[0] == "*" and line[1] == " ") or (line[0] == "-" and line[1] == " "):
            return "unordered_list"
        else:
            break

    # Detecting ordered list
    i = 1
    while i < len(block_lines):
        for line in block_lines:
            if not line[0].isdigit():
                i = len(block_lines)
            elif int(line[0]) == i and line[1] == "." and line[2] == " ":
                if i == len(block_lines):
                    return "ordered_list"

                else:
                    i += 1
            else:
                print("NOT a proper ordered list.")
                i = len(block_lines)

    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "ordered_list":
        return olist_to_html_node(block)
    if block_type == "unordered_list":
        return ulist_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
