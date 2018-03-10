from markdown import Markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


class MarkdownParser:
    """ Takes unicode strings and turns them into html

    Usage:
    ```
    with MarkdownParser(your_markdown_string) as md:
        print(md.html)
    ```
    """

    markdown_parser = Markdown(extensions=[GithubFlavoredMarkdownExtension()])

    def __init__(self, unparsed_text):
        self.unparsed_text = unparsed_text
        self.html = self.markdown_parser.convert(unparsed_text)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.markdown_parser.reset()
