from loader.base_loaders import BodyPageLoader
from my_dataclass.body_page import BodyPage
from parse_rule.rule import WebsiteSettingRule
import playwright_websession


class PlaywrightBodyPageLoader(BodyPageLoader):
    @staticmethod
    async def fetch_html(session: playwright_websession.WebSession, _: WebsiteSettingRule, body_page: BodyPage) -> None:
        page, encoding = await session.request_text(body_page.url)
        body_page.web_content.page = page
        body_page.web_content.encoding = encoding
