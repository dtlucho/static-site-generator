from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"No closing delimiter {delimiter} found in text '{old_node.text}'")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            node_type = TextType.NORMAL if i % 2 == 0 else text_type
            new_nodes.append(TextNode(sections[i], node_type))
    return new_nodes