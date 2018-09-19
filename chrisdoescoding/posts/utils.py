from markdown import Markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from django.utils.safestring import mark_safe


class MarkdownParser:
    """ Takes unicode strings and turns them into html

    Usage:
    ```
    with MarkdownParser(your_markdown_string) as md:
        print(md.html)
    ```
    """

    markdown_parser = Markdown(extensions=[GithubFlavoredMarkdownExtension()])

    def __init__(self, unparsed_text: str) -> None:
        self.unparsed_text: str = unparsed_text
        self.html: str = mark_safe(self.markdown_parser.convert(unparsed_text))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.markdown_parser.reset()
