from typing import Union

from playwright.async_api import ElementHandle

from my_dataclass.base_page import PageData


class IndexPageData(PageData):
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    """
    def __init__(self, url: Union[str, ElementHandle], page_id: int):
        """

        :param url: 目录页的某个 page，每个 page 对应一个 url
        :param page_id: 目录页的页码
        """
        super().__init__(url, page_id)

        self.urls = []
        # TODO: 一个 chapter 即章节可能好几页
        self.chapters_names = []
