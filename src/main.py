from textnode import TextNode, TextType

def main():
    print("hello world")
    textnode = TextNode("hello", TextType.NORMAL, "https://www.google.com")
    print(textnode)

main()