import os
from block_markdown import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        content = f.read()
        html_string = markdown_to_html_node(content).to_html()
        page_title = extract_title(content)

    with open(template_path, "r") as f:
        template = f.read()
        template = template.replace("{{ Title }}", page_title)
        template = template.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    list_of_files = os.listdir(dir_path_content)
    for file in list_of_files:
        if file.endswith(".md"):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file.replace(".md", ".html")))
        elif os.path.isdir(os.path.join(dir_path_content, file)):
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
        else:
            raise ValueError(f"invalid file: {file}")

