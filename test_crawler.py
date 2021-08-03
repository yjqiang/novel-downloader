import asyncio
from urllib.parse import urlparse

import dict_str_class
from config_loader import config_loader
from my_dataclass.body_page import BodyPage
from parse_rule.rule import WebsiteRule
import log


async def main():
    log.init()
    rules = {element['netloc']: WebsiteRule(element) for element in config_loader.rule['websites']}

    url = 'http://www.hejixs.com/113/113311/7150266_2.html'
    # url = 'https://www.xbookcn.com/book/chest/2.htm'
    rule: WebsiteRule = rules[urlparse(url).netloc]

    session = dict_str_class.web_sessions[rule.all_rules_of_1_website['body_page']['loader']]()
    await session.init()

    body_page = BodyPage(url, chapter_id=0)
    BodyPageLoader = dict_str_class.body_page_loaders[rule.all_rules_of_1_website['body_page']['loader']]
    await BodyPageLoader.fetch_html(session, rule.website_setting_rule, body_page)
    print(f'{body_page.web_content.encoding=}')
    await BodyPageLoader.get_title(body_page=body_page, body_page_rule=rule.body_page_rule)
    print(f'{body_page.title=}')
    await BodyPageLoader.get_content(body_page=body_page, body_page_rule=rule.body_page_rule)
    print(f'{[str(paragraph) for paragraph in body_page.content]=}')
    await BodyPageLoader.get_next_page_url(body_page=body_page, body_page_rule=rule.body_page_rule)
    print(f'{body_page.next_page_url=}')
    session.set_state(body_page.web_content.page, False)  # 完事了

    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
