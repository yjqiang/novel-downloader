import asyncio
from urllib.parse import urlparse

import dict_str_class
from config_loader import config_loader
from my_dataclass.body_page import BodyPageData
from my_dataclass.index_page import IndexPageData
from parse_rule.rule import WebsiteRule
import log


async def main():
    log.init()
    rules = {element['netloc']: WebsiteRule(element) for element in config_loader.rule['websites']}

    url = 'https://www.xbookcn.com/book/chest/1.htm'
    url = 'http://m.haohengwx.com/16/16248/177341.html'
    # url = 'http://www.hejixs.com/113/113311/7150266_2.html'
    rule: WebsiteRule = rules[urlparse(url).netloc]

    session = dict_str_class.web_sessions[rule.all_rules_of_1_website['body_page']['loader']]()
    await session.init()

    body_page_data = BodyPageData(url, page_id=0)
    BodyPageLoader = dict_str_class.body_page_loaders[rule.all_rules_of_1_website['body_page']['loader']]
    await BodyPageLoader.fetch_html(session, rule.website_setting_rule, body_page_data)
    while True:
        print('>>>')
        print(f'{body_page_data.url=}')
        print(f'{body_page_data.raw_page_data.encoding=}')
        await BodyPageLoader.get_title(body_page=body_page_data, body_page_rule=rule.body_page_rule)
        print(f'{body_page_data.title=}')
        await BodyPageLoader.get_content(body_page=body_page_data, body_page_rule=rule.body_page_rule)
        print(f'{[str(paragraph) for paragraph in body_page_data.content]=}')
        await BodyPageLoader.get_next_page_url(body_page=body_page_data, body_page_rule=rule.body_page_rule)
        print(f'{body_page_data.next_page_url=}')

        if body_page_data.next_page_url is None:
            break

        # 下一页的 page
        next_body_page_data = await BodyPageLoader.goto_next_page(session=session, website_setting_rule=rule.website_setting_rule, cur_body_page=body_page_data)  # 跳到下一页
        print(f'{body_page_data.url} => {next_body_page_data.url}')
        if body_page_data.next_page_url == body_page_data.url:  # 有的网站仅仅会一直重复最后页
            break

        body_page_data = next_body_page_data

        if body_page_data.page_id >= 5:
            break

    await session.close()

    print('#################################################################################################')

    url = 'https://www.xbookcn.com/book/chest/index.htm'
    url = 'http://m.haohengwx.com/16/16248/'
    # url = 'http://www.hejixs.com/113/113311_1/'
    rule: WebsiteRule = rules[urlparse(url).netloc]
    print(rule.website_setting_rule.headers)

    session = dict_str_class.web_sessions[rule.all_rules_of_1_website['index_page']['loader']]()
    await session.init()

    index_page_data = IndexPageData(url, page_id=0)
    IndexPageLoader = dict_str_class.index_page_loaders[rule.all_rules_of_1_website['index_page']['loader']]
    await IndexPageLoader.fetch_html(session, rule.website_setting_rule, index_page_data)
    while True:
        print('>>>')
        print(f'{index_page_data.url=}')
        print(f'{index_page_data.raw_page_data.encoding=}')
        await IndexPageLoader.get_content(index_page=index_page_data, index_page_rule=rule.index_page_rule)
        print(f'{[(url, chapter_name) for url, chapter_name in zip(index_page_data.urls, index_page_data.chapters_names)]=}')
        await IndexPageLoader.get_next_page_url(index_page=index_page_data, index_page_rule=rule.index_page_rule)
        print(f'{index_page_data.next_page_url=}')

        if index_page_data.next_page_url is None:
            break

        # 下一页的 page
        next_index_page_data = await IndexPageLoader.goto_next_page(session=session, website_setting_rule=rule.website_setting_rule, cur_index_page=index_page_data)  # 跳到下一页
        print(f'{index_page_data.url} => {next_index_page_data.url=}')
        if index_page_data.next_page_url == index_page_data.url:  # 有的网站仅仅会一直重复最后页
            break

        index_page_data = next_index_page_data

        if index_page_data.page_id >= 5:
            break

    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
