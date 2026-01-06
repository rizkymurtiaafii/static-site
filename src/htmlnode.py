class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return " " + props_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value to convert to HTML.")
        if not self.tag:
            return self.value
        
        props_str = ''
        if self.props:
            for key, value in self.props.items():
                props_str += f' {key}="{value}"'

        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML.")
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML.")
        
        children_html = ''
        for child in self.children:
            children_html += child.to_html()

        props_str = ''
        if self.props:
            for key, value in self.props.items():
                props_str += f' {key}="{value}"'

        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"