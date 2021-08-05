from typing import Optional

from lxml import html, etree
from playwright.async_api import ElementHandle

from my_dataclass.base_page import RawPageData
from parse_rule.base_low_rules import HtmlElementRule, BodyPageContentHtmlElementRule


async def _find(str_pattern: str, raw_page_data: RawPageData) -> Optional[html.HtmlElement]:
    result = await raw_page_data.page.query_selector(str_pattern)
    if result is None or not await result.is_visible():
        return None
    return html.fromstring(await result.evaluate('element => element.outerHTML'), parser=etree.HTMLParser(remove_comments=True))


async def _findall(str_pattern: str, raw_page_data: RawPageData) -> list[html.HtmlElement]:
    find_result = await raw_page_data.page.query_selector_all(str_pattern)
    result = []
    for element in find_result:
        if await element.is_visible():
            result.append(html.fromstring(await element.evaluate('element => element.outerHTML'), parser=etree.HTMLParser(remove_comments=True)))
    return result


class PlaywrightHtmlElementRule(HtmlElementRule):
    """
    利用 Playwright 的搜索
    """
    async def find(self, raw_page_data: RawPageData) -> Optional[html.HtmlElement]:
        return await _find(self.str_pattern, raw_page_data)

    async def findall(self, raw_page_data: RawPageData) -> list[html.HtmlElement]:
        return await _findall(self.str_pattern, raw_page_data)


class BodyPageContentPlaywrightHtmlElementRule(BodyPageContentHtmlElementRule):
    """
    利用 Playwright 的搜索
    """
    async def find(self, raw_page_data: RawPageData) -> Optional[html.HtmlElement]:
        return await _find(self.str_pattern, raw_page_data)

    async def findall(self, raw_page_data: RawPageData) -> list[html.HtmlElement]:
        return await _findall(self.str_pattern, raw_page_data)


class PlaywrightClickRule:
    """
    例如有的下一页没有显式的跳转 url，只有 click 了才知道
    """
    def __init__(self, str_pattern: str):
        """

        :param str_pattern:
        """
        self.str_pattern = str_pattern

    async def find(self, raw_page_data: RawPageData) -> Optional[ElementHandle]:
        result = await raw_page_data.page.query_selector(self.str_pattern)
        if result is None or not await result.is_visible():
            return None
        return result

    async def findall(self, raw_page_data: RawPageData) -> list[ElementHandle]:
        find_result = await raw_page_data.page.query_selector_all(self.str_pattern)
        return [element for element in find_result if await element.is_visible()]

    async def find_attr(self, raw_page_data: RawPageData) -> Optional[list[ElementHandle]]:
        """
        为了统一 api
        :param raw_page_data:
        :return:
        """
        find_result = await self.find(raw_page_data)
        if find_result is None:
            return None
        return [find_result]

    async def findall_attr(self, raw_page_data: RawPageData) -> list[list[ElementHandle]]:
        """
        为了统一 api
        :param raw_page_data:
        :return:
        """
        return [[find_result] for find_result in await self.findall(raw_page_data)]
