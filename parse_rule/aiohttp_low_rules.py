"""
虽然名字是 aiohttp，其实准确的来说是 lxml_low_rules 因为直接操作对象是 lxml.css_selector 进行 find 和 findall
"""
from typing import Optional

from lxml import cssselect

from my_dataclass.base_page import RawPageData
from parse_rule.base_low_rules import ElementRule, BodyPageContentElementRule
from utils import etree_Element


async def _find(css_selector_pattern: cssselect.CSSSelector, raw_page_data: RawPageData) -> Optional[etree_Element]:
    result = css_selector_pattern(raw_page_data.root)
    if result:
        return result[0]
    return None


async def _findall(css_selector_pattern: cssselect.CSSSelector, raw_page_data: RawPageData) -> list[etree_Element]:
    return css_selector_pattern(raw_page_data.root)


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
