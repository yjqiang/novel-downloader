from typing import Optional

from lxml import html, etree

from my_dataclass.body_page import WebContent
from parse_rule.base_low_rules import LxmlHtmlElementRule, BodyPageContentLxmlHtmlElementRule


class PlaywrightLxmlHtmlElementRule(LxmlHtmlElementRule):
    async def find(self, web_content: WebContent) -> Optional[html.HtmlElement]:
        result = await web_content.page.query_selector(self.str_pattern)
        if result is None or not await result.is_visible():
            return None
        return html.fromstring(await result.evaluate('element => element.outerHTML'), parser=etree.HTMLParser(remove_comments=True))

    async def findall(self, web_content: WebContent) -> list[html.HtmlElement]:
        find_result = await web_content.page.query_selector_all(self.str_pattern)
        result = []
        for element in find_result:
            if await element.is_visible():
                result.append(html.fromstring(await element.evaluate('element => element.outerHTML'), parser=etree.HTMLParser(remove_comments=True)))
        return result


class BodyPageContentPlaywrightLxmlHtmlElementRule(BodyPageContentLxmlHtmlElementRule):
    async def find(self, web_content: WebContent) -> Optional[html.HtmlElement]:
        result = await web_content.page.query_selector(self.str_pattern)
        if result is None or not await result.is_visible():
            return None
        return html.fromstring(await result.evaluate('element => element.outerHTML'), parser=etree.HTMLParser(remove_comments=True))

    async def findall(self, web_content: WebContent) -> list[html.HtmlElement]:
        find_result = await web_content.page.query_selector_all(self.str_pattern)
        result = []
        for element in find_result:
            if await element.is_visible():
                result.append(html.fromstring(await element.evaluate('element => element.outerHTML'), parser=etree.HTMLParser(remove_comments=True)))
        return result
