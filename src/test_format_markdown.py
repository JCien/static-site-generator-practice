import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_image,
    text_type_link,
    text_type_code,
)

from format_markdown import (
    text_to_text_nodes,
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_sample(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

        old_nodes = [TextNode("a|b|c", text_type_text)]
        result_nodes = split_nodes_delimiter(old_nodes, "|", text_type_text)
        expected_nodes = [
            TextNode("a", text_type_text),
            TextNode("b", text_type_text),
            TextNode("c", text_type_text),
        ]
        self.assertEqual(result_nodes, expected_nodes)

        old_nodes = [TextNode("a|b|c", text_type_text)]
        result_nodes = split_nodes_delimiter(old_nodes, "|", text_type_bold)
        expected_nodes = [
            TextNode("a", text_type_text),
            TextNode("b", text_type_bold),
            TextNode("c", text_type_text),
        ]
        self.assertEqual(result_nodes, expected_nodes)

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("a|b|c|d", text_type_text)], "|", text_type_text
            )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        input_text = "This is **bold** and *italic* and `code`."
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" and ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(".", text_type_text),
        ]
        output = text_to_text_nodes(input_text)
        assert (
            output == expected_output
        ), f"Case 1 Failed: Expected {expected_output}, but got {output}"

        input_text = "This is plain text."
        expected_output = [TextNode("This is plain text.", text_type_text)]
        output = text_to_text_nodes(input_text)
        assert (
            output == expected_output
        ), f"Case 2 Failed: Expected {expected_output}, but got {output}"

        input_text = "**bold** and **another bold**."
        expected_output = [
            TextNode("bold", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("another bold", text_type_bold),
            TextNode(".", text_type_text),
        ]
        output = text_to_text_nodes(input_text)
        assert (
            output == expected_output
        ), f"Case 7 Failed: Expected {expected_output}, but got {output}"


if __name__ == "__main__":
    unittest.main()
