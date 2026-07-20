from __future__ import annotations
from enum import Enum
from htmlnode import *
import re
"""
TextNode is a simple representation of data. Nothing HTML yet. Is a structure used to later on build needed HTML.
"""


class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, TextNode):
            return all([
                self.text == other.text,
                self.text_type == other.text_type,
                self.url == other.url
            ])
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    @staticmethod
    def _split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
        new_nodes: list[TextNode] = []
        for old_node in old_nodes:
            if old_node.text_type is not TextType.TEXT:
                new_nodes.append(old_node)
                continue
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("This seems like invalid markdown language. Are missing delimiters.")
            for i in range(len(parts)):
                part = parts[i]
                new_type = text_type if i % 2 == 1 else TextType.TEXT
                new_nodes.append(TextNode(part, new_type))

        return new_nodes

    @staticmethod
    def _split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
        result: list[TextNode] = []
        
        for old_node in old_nodes:
            if old_node.text_type is not TextType.TEXT:
                result.append(old_node)
                continue
            text = old_node.text
            images = TextNode._extract_markdown_images(text)
            if len(images) == 0:
                result.append(old_node)
                continue
            
            for image in images:
                parts = text.split(f"![{image[0]}]({image[1]})", 1)
                if parts[0] != "":
                    result.append(TextNode(parts[0], TextType.TEXT))
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))    
                text = parts[1]
            if text != "":
                result.append(TextNode(text, TextType.TEXT))
        return result

    @staticmethod
    def _split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
        result: list[TextNode] = []
        
        for old_node in old_nodes:
            if old_node.text_type is not TextType.TEXT:
                result.append(old_node)
                continue
            text = old_node.text
            links = TextNode._extract_markdown_links(text)
            if len(links) == 0:
                result.append(old_node)
                continue
            
            for link in links:
                parts = text.split(f"[{link[0]}]({link[1]})", 1)
                if parts[0] != "":
                    result.append(TextNode(parts[0], TextType.TEXT))
                result.append(TextNode(link[0], TextType.LINK, link[1]))    
                text = parts[1]
            if text != "":
                result.append(TextNode(text, TextType.TEXT))
        return result

    @staticmethod
    def _extract_markdown_images(text: str) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = []
        names = re.findall(r"!\[([a-zA-Z\s]+)\]\(\S+\)", text)
        links = re.findall(r"!\[[a-zA-Z0-9\s]+\]\((\S+)\)", text)
        if len(names) != len(links):
            raise Exception("Something went wrong")

        for i in range(len(names)):
            result.append((names[i], links[i]))
        return result

    @staticmethod
    def _extract_markdown_links(text: str) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = []
        alts = re.findall(r"\[([a-zA-Z\s]+)\]\(\S+\)", text)
        urls = re.findall(r"\[[a-zA-Z0-9\s]+\]\((\S+)\)", text)
        if len(alts) != len(urls):
            raise Exception("Something went wrong")

        for i in range(len(alts)):
            result.append((alts[i], urls[i]))
        return result

    @classmethod
    def text_to_textnodes(cls, text: str) -> list[TextNode]:
        result: list[TextNode] = [TextNode(text, TextType.TEXT)]

        result =  cls._split_nodes_delimiter(result, "**", TextType.BOLD)
        result =  cls._split_nodes_delimiter(result, "_", TextType.ITALIC)
        result =  cls._split_nodes_delimiter(result, "`", TextType.CODE)
        result =  cls._split_nodes_image(result)
        result = cls._split_nodes_link(result)

        return result



    

    




