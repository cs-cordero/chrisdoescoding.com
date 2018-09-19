from django.utils.safestring import mark_safe

from markdown import Markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

from typing import Any

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

    def __enter__(self) -> 'MarkdownParser':
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self.markdown_parser.reset()
