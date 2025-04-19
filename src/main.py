import os
from copy_directory import copy_directory
from generate_page import generate_pages_recursive

static_dir_path = "./static"
public_dir_path = "./public"
content_dir_path = "./content"
template_path = "./template.html"


def main():
    copy_directory(static_dir_path, public_dir_path)
    generate_pages_recursive(content_dir_path, template_path, public_dir_path)


main()
