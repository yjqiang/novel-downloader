from dataclasses import dataclass
from typing import Optional

from lxml import html
from playwright.async_api import Page


@dataclass
class WebContent:
    str_html: Optional[str] = None  # 网页的 HTML
    root: Optional[html.HtmlElement] = None  # 网页的 HTML 解析
    page: Optional[Page] = None  # playwright 的 page
    encoding: Optional[str] = None  # 编码


class BodyPage:
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    """
    def __init__(self, url: str, chapter_id: int):
        """

        :param url: 正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
        :param chapter_id: 章节的 id，可能多个 page 共享一个 chapter_id，这时候表示网站把每一章节又细分了，分成了更细粒度的东西（一般叫页）
        """
        self.url = url
        self.chapter_id = chapter_id

        self.title = None
        self.content = None
        self.next_page_url = None

        self.web_content = WebContent()
