"""
虽然名字是 aiohttp，其实准确的来说是 html_low_rules 因为直接操作对象是网页 html，利用 lxml.css_selector 或者 lxml.xpath 进行 find 和 findall
"""
from typing import Optional, Union

from lxml import cssselect, etree

from my_dataclass.base_page import RawPageData
from parse_rule.base_low_rules import ElementRule, BodyPageContentElementRule
from utils import etree_Element


async def _find(pattern: Union[cssselect.CSSSelector, etree.XPath], raw_page_data: RawPageData) -> Optional[etree_Element]:
    result = pattern(raw_page_data.root)
    if result:
        return result[0]
    return None


async def _findall(pattern: Union[cssselect.CSSSelector, etree.XPath], raw_page_data: RawPageData) -> list[etree_Element]:
    return pattern(raw_page_data.root)


class LxmlCssElementRule(ElementRule):
    """
    CSS3
    利用 lxml 的 css_select 搜索
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        super().__init__(str_pattern, attributes)
        self.css_selector_pattern = cssselect.CSSSelector(str_pattern)

    async def find(self, raw_page_data: RawPageData) -> Optional[etree_Element]:
        return await _find(self.css_selector_pattern, raw_page_data)

    async def findall(self, raw_page_data: RawPageData) -> list[etree_Element]:
        return await _findall(self.css_selector_pattern, raw_page_data)


class LxmlXpathElementRule(ElementRule):
    """
    利用 lxml 的 Xpath 搜索
    注意 xpath 其实是可以支持直接返回 string 这些的，例如下例

    from lxml import etree

    root = etree.HTML("<root><a>TEXT</a></root>")
    find_text = etree.XPath("//text()")
    print(find_text(root))

    但是这里我们要求还是必须返回 etree_Element
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        super().__init__(str_pattern, attributes)
        self.xpath_pattern = etree.XPath(str_pattern)

    async def find(self, raw_page_data: RawPageData) -> Optional[etree_Element]:
        return await _find(self.xpath_pattern, raw_page_data)

    async def findall(self, raw_page_data: RawPageData) -> list[etree_Element]:
        return await _findall(self.xpath_pattern, raw_page_data)


class BodyPageContentLxmlCssElementRule(BodyPageContentElementRule):
    """
    CSS3
    利用 lxml 的 css_select 搜索
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        super().__init__(str_pattern, attributes)
        self.css_selector_pattern = cssselect.CSSSelector(str_pattern)

    async def find(self, raw_page_data: RawPageData) -> Optional[etree_Element]:
        return await _find(self.css_selector_pattern, raw_page_data)

    async def findall(self, raw_page_data: RawPageData) -> list[etree_Element]:
        return await _findall(self.css_selector_pattern, raw_page_data)


class BodyPageContentLxmlXpathElementRule(BodyPageContentElementRule):
    """
    利用 lxml 的 Xpath 搜索
    注意 xpath 其实是可以支持直接返回 string 这些的，例如下例

    from lxml import etree

    root = etree.HTML("<root><a>TEXT</a></root>")
    find_text = etree.XPath("//text()")
    print(find_text(root))

    但是这里我们要求还是必须返回 etree_Element
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        super().__init__(str_pattern, attributes)
        self.xpath_pattern = etree.XPath(str_pattern)

    async def find(self, raw_page_data: RawPageData) -> Optional[etree_Element]:
        return await _find(self.xpath_pattern, raw_page_data)

    async def findall(self, raw_page_data: RawPageData) -> list[etree_Element]:
        return await _findall(self.xpath_pattern, raw_page_data)
