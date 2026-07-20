from __future__ import annotations

class HTMLNode():
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict[str, str] | None = None
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, HTMLNode):
            return all([
                self.tag == other.tag,
                self.value == other.value,
                self.children == other.children,
                self.props == other.props
            ])
        return False

    def to_html(self) -> str:
        output = self.value or ""
        tag = self.tag or ""
        if self.children:
            output = ""
            tag = "div"
            for child in self.children:
                output += child.to_html()

        if tag > "":
            output = f"<{tag}{self.props_to_html()}>{output}</{tag}>"
        return output
    

    def props_to_html(self) -> str:
        result = ""
        if self.props:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value})"

        


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(
            self, 
            tag: str, 
            children: list["HTMLNode"], 
            props: dict[str, str] | None = None
        ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag is missing")
        if not self.children:
            raise ValueError("No children")

        result = ""
        for child in self.children:
            result += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
