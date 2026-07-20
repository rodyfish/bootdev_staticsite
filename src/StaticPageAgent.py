from __future__ import annotations
from textnode import TextNode, TextType
from htmlnode import *
from block import Block, BlockType
from file_handler import read_file, write_file, get_files_info
import re
import os


def textnode_to_htmlnode(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            props = {"href": text_node.url} if text_node.url else None
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text} if text_node.url else None
            return LeafNode("img", "", props)
        
        case _:
            raise Exception("Error with Node")
        

def text_to_leafnodes(text: str) -> list[LeafNode]:
    text_nodes = TextNode.text_to_textnodes(text)
    leaf_nodes: list[LeafNode] = []
    for text_node in text_nodes:
        leaf_node = textnode_to_htmlnode(text_node)
        leaf_nodes.append(leaf_node)

    return leaf_nodes


def block_to_htmlnode(block: Block) -> HTMLNode:
    if block.type == BlockType.PARAGRAPH:
        leafs: list[LeafNode] = []
        content = block.content.replace("\n", " ")
        
        leaf_nodes = text_to_leafnodes(content)
        node = ParentNode("p", leaf_nodes)
        return node
    
    if block.type == BlockType.CODE:
        return ParentNode("pre", [LeafNode("code", block.content)])
    
    if block.type == BlockType.QUOTE:
        leafs = text_to_leafnodes(block.content)
        return ParentNode("blockquote", leafs)
        
    if block.type == BlockType.OLIST:
        list_items = []
        for line in block.content.splitlines():
            leafs = text_to_leafnodes(line)
            list_items.append(ParentNode("li", leafs))
        return ParentNode("ol", list_items)
    
    if block.type == BlockType.ULIST:
        list_items = []
        for line in block.content.splitlines():
            leafs = text_to_leafnodes(line)
            list_items.append(ParentNode("li", leafs))
        return ParentNode("ul", list_items)
    
    if block.type == BlockType.HEADING:
        parts = block.content.split(" ", 1)
        leafs = text_to_leafnodes(parts[1])
        return ParentNode(f"h{len(parts[0])}", leafs)

    raise Exception("something went wrong")



def markdown_to_blocks(markdown:str) -> list[Block]:
    raw_blocks = markdown.split("\n\n")
    blocks: list[Block] = []

    for raw_block in raw_blocks:
        if raw_block == "":
            continue;
        
        if re.search(r"^[#]{1,6}\s", raw_block):
            blocks.append(Block(BlockType.HEADING, raw_block))
            continue
        
        if raw_block.startswith("```\n") and raw_block.endswith("```"):
            content = raw_block.split("```\n")[1]
            content = content.split("```")[0]
            blocks.append(Block(BlockType.CODE, content))
            continue
            
        quote_check = True
        unordered_check = True
        ordered_check = True
        count = 0
        for line in raw_block.splitlines():
            count += 1
            quote_check = quote_check and line.startswith(">")
            unordered_check = unordered_check and line.startswith("- ")
            ordered_check = ordered_check and line.startswith(f"{count}. ")

        if quote_check:
            content = "\n".join(list(map(lambda x: x[1:], raw_block.split("\n"))))
            blocks.append(Block(BlockType.QUOTE, content.replace("\n", "").strip()))
            continue
        if unordered_check:
            content = "\n".join(list(map(lambda x: x[2:], raw_block.split("\n"))))
            blocks.append(Block(BlockType.ULIST, content))
            continue
        if ordered_check:
            content = "\n".join(list(map(lambda x: x.split(" ", 1)[1], raw_block.split("\n"))))
            blocks.append(Block(BlockType.OLIST, content))
            continue

        blocks.append(Block(BlockType.PARAGRAPH, raw_block))
    
    return blocks
    
    
def markdown_to_htmlnode(markdown: str) -> HTMLNode:
    #Converting md to blocks
    blocks = markdown_to_blocks(markdown.strip("\n"))
    html_nodes: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_htmlnode(block)
        html_nodes.append(html_node)
  
    node = HTMLNode("div", None, html_nodes)
    return node


def extract_title(markdown: str) -> str:
    result = ""
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        if block.type == BlockType.HEADING and block.content.startswith("# "):
            return block.content[2:]

    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    md = read_file(from_path)
    template = read_file(template_path)
    title = extract_title(md)
    print("generating file..", from_path, template_path, dest_path)
    html = markdown_to_htmlnode(md).to_html()
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    write_file(".", dest_path, final_html)


    pass

def generate_page_recursive(path_content, template_path, dest_path):
    
    if not os.path.isdir:
        raise Exception (f'Error: "{path_content}" is not a dir')
    print("recurseive", path_content, template_path, dest_path)
    file_paths = os.listdir(path_content)
    for file_path in file_paths:
        file_dir = os.path.join(path_content, file_path)
        dest_dir = os.path.join(dest_path, file_path.replace(".md", ".html"))
        print("file", file_dir)
        if os.path.isfile(file_dir) and file_dir.split(".", -1)[1] == "md":
            generate_page(file_dir, template_path, dest_dir)
        elif os.path.isdir(file_dir):
            generate_page_recursive(file_dir, template_path, dest_dir)
        