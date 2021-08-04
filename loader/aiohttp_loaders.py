from collections import Callable
from urllib.parse import urljoin

from lxml import html, etree

from loader.base_loaders import BodyPageLoader, IndexPageLoader
from my_dataclass.base_page import PageData
from my_dataclass.index_page import IndexPageData
from my_dataclass.body_page import BodyPageData
from parse_rule.rule import WebsiteSettingRule, BodyPageRule, IndexPageRule, PageRule
import aiohttp_websession


async def _fetch_html(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, page_data: PageData) -> None:
    text_rsp, encoding = await session.request_text('GET', page_data.url, headers=website_setting_rule.headers, encoding=website_setting_rule.encoding)
    page_data.raw_page_data.str_html = text_rsp
    page_data.raw_page_data.encoding = encoding
    page_data.raw_page_data.root = html.fromstring(text_rsp, parser=etree.HTMLParser(remove_comments=True))


async def _get_next_page_url(page_rule: PageRule, page_data: PageData) -> None:
    next_page_url_rules = page_rule.next_page_url_rules
    for next_page_url_rule in next_page_url_rules:
        result = await next_page_url_rule.find_attr(page_data.raw_page_data)
        if result is not None:
            link = result[0]
            page_data.next_page_url = urljoin(page_data.url, link)
            return


async def _goto_next_page(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, cur_page_data: PageData,
                          next_page_data: PageData, fetch_html: Callable) -> None:
    assert isinstance(cur_page_data.next_page_url, str)
    await fetch_html(session, website_setting_rule, next_page_data)


class AiohttpBodyPageLoader(BodyPageLoader):
    @staticmethod
    async def fetch_html(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, body_page: BodyPageData) -> None:
        return await _fetch_html(session, website_setting_rule, body_page)

    @staticmethod
    async def get_next_page_url(body_page_rule: BodyPageRule, body_page: BodyPageData) -> None:
        return await _get_next_page_url(body_page_rule, body_page)

    @staticmethod
    async def goto_next_page(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, cur_body_page: BodyPageData) -> BodyPageData:
        next_page_data = BodyPageData(url=cur_body_page.next_page_url, page_id=cur_body_page.page_id + 1)
        await _goto_next_page(session, website_setting_rule, cur_body_page, next_page_data, AiohttpBodyPageLoader.fetch_html)
        return next_page_data


class AiohttpIndexPageLoader(IndexPageLoader):
    @staticmethod
    async def fetch_html(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, index_page: IndexPageData) -> None:
        return await _fetch_html(session, website_setting_rule, index_page)

    @staticmethod
    async def get_next_page_url(index_page_rule: IndexPageRule, index_page: IndexPageData) -> None:
        return await _get_next_page_url(index_page_rule, index_page)

    @staticmethod
    async def goto_next_page(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, cur_index_page: IndexPageData) -> IndexPageData:
        next_page_data = IndexPageData(url=cur_index_page.next_page_url, page_id=cur_index_page.page_id + 1)
        await _goto_next_page(session, website_setting_rule, cur_index_page, next_page_data, AiohttpIndexPageLoader.fetch_html)
        return next_page_data
