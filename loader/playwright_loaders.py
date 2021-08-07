from collections import Callable
from urllib.parse import urljoin

from playwright.async_api import ElementHandle

from loader.base_loaders import BodyPageLoader, IndexPageLoader
from my_dataclass.base_page import PageData
from my_dataclass.body_page import BodyPageData
from my_dataclass.index_page import IndexPageData
from parse_rule.rule import WebsiteSettingRule, BodyPageRule, IndexPageRule, PageRule
import playwright_websession


async def _fetch_html(session: playwright_websession.WebSession, _: WebsiteSettingRule, page_data: PageData) -> None:
    page, encoding = await session.request_text(page_data.url, page_data.raw_page_data.page)
    page_data.raw_page_data.page = page
    page_data.raw_page_data.encoding = encoding


async def _get_next_page_url(page_rule: PageRule, page_data: PageData) -> None:
    next_page_url_rules = page_rule.next_page_url_rules
    for next_page_url_level, next_page_url_rule in enumerate(next_page_url_rules, start=1-len(next_page_url_rules)):
        result = await next_page_url_rule.find_attr(page_data.raw_page_data)
        if result is not None:
            # 0 表示最后一层（例如：下一章），-1 表示倒数第二层（例如：下一页）
            page_data.next_page_url_level = next_page_url_level

            link = result[0]
            # 参考 playwright_low_rules.PlaywrightClickRule，例如有的下一页没有显式的跳转 url，只有 click 了才知道
            assert isinstance(link, (str, ElementHandle))
            if isinstance(link, str):
                page_data.next_page_url = urljoin(page_data.url, link)
            else:
                page_data.next_page_url = link
            return


async def _goto_next_page(session: playwright_websession.WebSession, website_setting_rule: WebsiteSettingRule, cur_page_data: PageData,
                          next_page_data: PageData, fetch_html: Callable) -> None:
    """
    根据当前页的数据，获取下一页的真实 url 地址并加载
    :param session:
    :param website_setting_rule:
    :param cur_page_data:
    :return:
    """
    assert isinstance(cur_page_data.next_page_url, (str, ElementHandle))

    if isinstance(cur_page_data.next_page_url, str):
        session.set_state(cur_page_data.raw_page_data.page, True)  # 让出
        await fetch_html(session, website_setting_rule, next_page_data)
    else:
        next_page_data.raw_page_data.page = cur_page_data.raw_page_data.page  # 当 url 是 ElementHandle 时候，playwright_websession 需要复用 page
        await fetch_html(session, website_setting_rule, next_page_data)
        # 改写 url 为真正的 str url
        url: str = next_page_data.raw_page_data.page.url
        assert isinstance(url, str)
        cur_page_data.next_page_url = url
        next_page_data.url = url


class PlaywrightBodyPageLoader(BodyPageLoader):
    @staticmethod
    async def fetch_html(session: playwright_websession.WebSession, website_setting_rule: WebsiteSettingRule, page_data: BodyPageData) -> None:
        return await _fetch_html(session, website_setting_rule, page_data)

    @staticmethod
    async def get_next_page_url(page_rule: BodyPageRule, page_data: BodyPageData) -> None:
        return await _get_next_page_url(page_rule, page_data)

    @staticmethod
    async def goto_next_page(session: playwright_websession.WebSession, website_setting_rule: WebsiteSettingRule, cur_page_data: BodyPageData) -> BodyPageData:
        next_page_data = BodyPageData(url=cur_page_data.next_page_url, page_id=cur_page_data.page_id + 1)
        await _goto_next_page(session, website_setting_rule, cur_page_data, next_page_data, PlaywrightBodyPageLoader.fetch_html)
        return next_page_data


class PlaywrightIndexPageLoader(IndexPageLoader):
    @staticmethod
    async def fetch_html(session: playwright_websession.WebSession, website_setting_rule: WebsiteSettingRule, page_data: IndexPageData) -> None:
        return await _fetch_html(session, website_setting_rule, page_data)

    @staticmethod
    async def get_next_page_url(page_rule: IndexPageRule, page_data: IndexPageData) -> None:
        return await _get_next_page_url(page_rule, page_data)

    @staticmethod
    async def goto_next_page(session: playwright_websession.WebSession, website_setting_rule: WebsiteSettingRule, cur_page_data: IndexPageData) -> IndexPageData:
        next_page_data = IndexPageData(url=cur_page_data.next_page_url, page_id=cur_page_data.page_id + 1)
        await _goto_next_page(session, website_setting_rule, cur_page_data, next_page_data, PlaywrightIndexPageLoader.fetch_html)
        return next_page_data
