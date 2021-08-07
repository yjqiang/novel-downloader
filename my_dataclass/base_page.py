from typing import Union, Optional
from dataclasses import dataclass

from playwright.async_api import Page, ElementHandle

from utils import etree_Element


@dataclass
class RawPageData:
    """
    底层未处理的数据，例如该网页的 HTML 等
    """
    str_html: Optional[str] = None  # 网页的 HTML
    root: Optional[etree_Element] = None  # 网页的 HTML 解析
    page: Optional[Page] = None  # playwright 的 page
    encoding: Optional[str] = None  # 编码


class PageData:
    """
    正文或目录某一页的全部数据，包括且不限于一个 WebContent、url、page_id 等
    """
    def __init__(self, url: Union[str, ElementHandle], page_id: int):
        """

        :param url: 目录页的某个 page，每个 page 对应一个 url
        :param page_id: 目录页的页码
        """
        self.url = url
        self.page_id = page_id

        # 为 None 表示结束了
        # 参考 playwright_low_rules.PlaywrightClickRule，例如有的下一页没有显式的跳转 url，只有 click 了才知道
        # 所以可能是 str_url 或者仅仅是个 ElementHandle 等待点击
        self.next_page_url: Optional[Union[str, ElementHandle]] = None
        self.next_page_url_level: int = 1  # 0 表示最后一层（例如：下一章），-1 表示倒数第二层（例如：下一页）

        self.raw_page_data = RawPageData()
