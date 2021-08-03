"""
虽然名字是 aiohttp，其实准确的来说是 lxml_low_rules 因为直接操作对象是 lxml.css_selector 进行 find 和 findall
"""
from typing import Optional

from lxml import html, cssselect

from my_dataclass.body_page import WebContent
from parse_rule.base_low_rules import LxmlHtmlElementRule, BodyPageContentLxmlHtmlElementRule


class AiohttpLxmlHtmlElementRule(LxmlHtmlElementRule):
    """
    CSS3
    从 root 里面 css_select 搜索
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        super().__init__(str_pattern, attributes)
        self.css_selector_pattern = cssselect.CSSSelector(str_pattern)

    async def find(self, web_content: WebContent) -> Optional[html.HtmlElement]:
        result = self.css_selector_pattern(web_content.root)
        if result:
            return result[0]
        return None

    async def findall(self, web_content: WebContent) -> list[html.HtmlElement]:
        return self.css_selector_pattern(web_content.root)


class BodyPageContentAiohttpLxmlHtmlElementRule(BodyPageContentLxmlHtmlElementRule):
    """
    CSS3
    从 root 里面 css_select 搜索
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        super().__init__(str_pattern, attributes)
        self.css_selector_pattern = cssselect.CSSSelector(str_pattern)

    async def find(self, web_content: WebContent) -> Optional[html.HtmlElement]:
        result = self.css_selector_pattern(web_content.root)
        if result:
            return result[0]
        return None

    async def findall(self, web_content: WebContent) -> list[html.HtmlElement]:
        return self.css_selector_pattern(web_content.root)