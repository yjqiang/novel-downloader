from lxml import html, etree

from loader.base_loaders import BodyPageLoader
from my_dataclass.body_page import BodyPage
from parse_rule.rule import WebsiteSettingRule
import aiohttp_websession


class AiohttpBodyPageLoader(BodyPageLoader):
    @staticmethod
    async def fetch_html(session: aiohttp_websession.WebSession, website_setting_rule: WebsiteSettingRule, body_page: BodyPage) -> None:
        text_rsp, encoding = await session.request_text('GET', body_page.url, headers=website_setting_rule.headers, encoding=website_setting_rule.encoding)
        body_page.web_content.str_html = text_rsp
        body_page.web_content.encoding = encoding
        body_page.web_content.root = html.fromstring(text_rsp, parser=etree.HTMLParser(remove_comments=True))
