"""
正文页
"""
from typing import Union

from playwright.async_api import ElementHandle

from my_dataclass.base_page import PageData


class BodyPageData(PageData):
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    """
    def __init__(self, url: Union[str, ElementHandle], page_id: int):
        """

        :param url: 正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
        :param page_id: 章节的 id，可能多个 page 共享一个 chapter_id，这时候表示网站把每一章节又细分了，分成了更细粒度的东西（一般叫页）
        """
        super().__init__(url, page_id)

        self.title = None
        self.content = None  # list[paragraph]
