from textnode import TextNode, TextType
from block import Block, BlockType
from htmlnode import *
from file_handler import move_files
from StaticPageAgent import generate_page_recursive







def main():
    move_files("static/", "public/")
    generate_page_recursive("content/", "template.html", "public/")

main()