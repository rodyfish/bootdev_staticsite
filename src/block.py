from __future__ import annotations
from enum import Enum
from htmlnode import *
from textnode import *
from typing import Any


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

class Block():
    def __init__(self, type: BlockType, content: str):
        self.type = type
        self.content = content

    def __repr__(self) -> str:
        return f"Block({self.type}, {self.content})"
    

