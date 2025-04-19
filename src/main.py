import os
from copy_directory import copy_directory
from generate_page import generate_page

static_dir_path = "./static"
public_dir_path = "./public"
content_dir_path = "./content"
template_path = "./template.html"


def main():
    copy_directory(static_dir_path, public_dir_path)
    generate_page(
        os.path.join(content_dir_path, "index.md"),
        template_path,
        os.path.join(public_dir_path, "index.html"),
    )


main()
