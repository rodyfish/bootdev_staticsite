from textnode import TextNode, TextType
from block import Block, BlockType
from htmlnode import *
from file_handler import move_files
from StaticPageAgent import generate_page_recursive
import sys






def main():
    basepath = "/"
    try:
        basepath = sys.argv[1]
    except:
        pass

    print(basepath)
    move_files("static/", "docs/")
    generate_page_recursive(basepath, "content/", "template.html", "docs/")

main()