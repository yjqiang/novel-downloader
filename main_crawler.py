import asyncio
from urllib.parse import urlparse

import dict_str_class
import utils
from config_loader import config_loader
from my_dataclass.body_page import BodyPage
from parse_rule.rule import WebsiteRule


async def main():
    rules = {element['netloc']: WebsiteRule(element) for element in config_loader.rule['websites']}

    url = 'http://www.hejixs.com/113/113311/7150266.html'
    # url = 'https://www.xbookcn.com/book/chest/1.htm'
    rule = rules[urlparse(url).netloc]

    session = dict_str_class.web_sessions[rule.all_rules_of_1_website['body_page']['loader']]()
    await session.init()

    BodyPageLoader = dict_str_class.body_page_loaders[rule.all_rules_of_1_website['body_page']['loader']]

    i = 0
    while True:
        print(f'HANDLING {i}')
        body_page = BodyPage(url, chapter_id=i)
        await BodyPageLoader.fetch_html(session, rule.website_setting_rule, body_page)  # download html and parse it
        await BodyPageLoader.get_title(body_page=body_page, body_page_rule=rule.body_page_rule)
        await BodyPageLoader.get_content(body_page=body_page, body_page_rule=rule.body_page_rule)
        await BodyPageLoader.get_next_page_url(body_page=body_page, body_page_rule=rule.body_page_rule)
        print(f'{body_page.web_content.encoding=}')
        print(f'{body_page.title=}')
        print(f'{[str(paragraph) for paragraph in body_page.content]=}')
        print(f'{body_page.next_page_url=}')

        session.set_state(body_page.web_content.page, True)  # 完事了

        utils.save_json(f'data/{i}.json',
                        {
                            'encoding': body_page.web_content.encoding,
                            'content': [paragraph.to_json() for paragraph in body_page.content],
                            'title': body_page.title
                        })

        if body_page.next_page_url is None or i >= 5:
            break
        url = body_page.next_page_url
        i += 1

    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
