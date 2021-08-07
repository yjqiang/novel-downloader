import asyncio
from typing import Type, Union
from urllib.parse import urlparse

import dict_str_class
from config_loader import config_loader
from my_dataclass.body_page import BodyPageData
from my_dataclass.index_page import IndexPageData
from loader.base_loaders import BodyPageLoader, IndexPageLoader
from parse_rule.rule import WebsiteRule
import playwright_websession
import aiohttp_websession
from my_dataclass.book import Book
from log import logger
import utils


async def parse_1_chapter_bodies(session: Union[playwright_websession.WebSession, aiohttp_websession.WebSession],
                                 start_url: str, rule: WebsiteRule, class_body_page_loader: Type[BodyPageLoader]) -> list[BodyPageData]:
    body_page_datas = []
    body_page_data = BodyPageData(start_url, page_id=0)
    await class_body_page_loader.fetch_html(session, rule.website_setting_rule, body_page_data)
    while True:
        await class_body_page_loader.get_title(page_data=body_page_data, page_rule=rule.body_page_rule)
        await class_body_page_loader.get_content(page_data=body_page_data, page_rule=rule.body_page_rule)
        await class_body_page_loader.get_next_page_url(page_data=body_page_data, page_rule=rule.body_page_rule)

        body_page_datas.append(body_page_data)  # 这里 body_page_data 还没处理完，例如真实 next_page_url 解析，但是没关系，后面对象的变量变了，list 里面该对象也是变的（指向同一个 object 的）

        if body_page_data.next_page_url is None or body_page_data.next_page_url_level == 0:  # next_page_url_level 为 0 说明跳到下一章了
            session.set_state(body_page_data.raw_page_data.page, True)
            break

        # 下一页的 page
        next_body_page_data = await class_body_page_loader.goto_next_page(session=session, website_setting_rule=rule.website_setting_rule, cur_page_data=body_page_data)  # 跳到下一页
        if body_page_data.next_page_url == body_page_data.url:  # 有的网站仅仅会一直重复最后页
            session.set_state(next_body_page_data.raw_page_data.page, True)
            break

        body_page_data = next_body_page_data

    return body_page_datas


async def parse_all_indices(session: Union[playwright_websession.WebSession, aiohttp_websession.WebSession],
                            start_url: str, rule: WebsiteRule, class_index_page_loader: Type[IndexPageLoader]) -> list[IndexPageData]:
    index_page_datas = []
    index_page_data = IndexPageData(start_url, page_id=0)
    await class_index_page_loader.fetch_html(session, rule.website_setting_rule, index_page_data)
    while True:
        await class_index_page_loader.get_content(page_data=index_page_data, page_rule=rule.index_page_rule)
        await class_index_page_loader.get_next_page_url(page_data=index_page_data, page_rule=rule.index_page_rule)

        index_page_datas.append(index_page_data)  # 这里 index_page_data 还没处理完，例如真实 next_page_url 解析，但是没关系，后面对象的变量变了，list 里面该对象也是变的（指向同一个 object 的）

        if index_page_data.next_page_url is None:
            session.set_state(index_page_data.raw_page_data.page, True)
            break

        # 下一页的 page
        next_index_page_data = await class_index_page_loader.goto_next_page(session=session, website_setting_rule=rule.website_setting_rule, cur_page_data=index_page_data)  # 跳到下一页
        logger.info(f'{index_page_data.url} => {next_index_page_data.url=}')
        if index_page_data.next_page_url == index_page_data.url:  # 有的网站仅仅会一直重复最后页
            session.set_state(next_index_page_data.raw_page_data.page, True)
            break

        index_page_data = next_index_page_data

    return index_page_datas


async def main():
    rules = {element['netloc']: WebsiteRule(element) for element in config_loader.rule['websites']}

    # url = 'https://www.xbookcn.com/book/chest/index.htm'
    # url = 'http://m.haohengwx.com/16/16248/'
    # url = 'http://www.hejixs.com/113/113311_1/'  # 这货的目录就不对，两个 index 指向同一章正文
    url = 'https://www.kunnu.com/zichuan/'
    rule = rules[urlparse(url).netloc]

    # 目录页处理
    # 目录页和正文页可能一个需要 playwright，另一个不需要，所以两者的 session 不 share
    class_index_page_loader = dict_str_class.index_page_loaders[rule.all_rules_of_1_website['index_page']['loader']]
    session = dict_str_class.web_sessions[rule.all_rules_of_1_website['index_page']['loader']]()
    await session.init()
    index_page_datas = await parse_all_indices(session, url, rule, class_index_page_loader)
    await session.close()

    indices = [(url, chapter_name) for index_page_data in index_page_datas for url, chapter_name in zip(index_page_data.urls, index_page_data.chapters_names)]

    logger.info(f'目录解析完毕，一共 {len(indices)} 章节')

    indices = indices[:30]
    ###################################################################################################################################################

    # 正文页处理
    # 根据 index 数据并发爬取数据
    results = []
    class_body_page_loader = dict_str_class.body_page_loaders[rule.all_rules_of_1_website['body_page']['loader']]
    session = dict_str_class.web_sessions[rule.all_rules_of_1_website['body_page']['loader']]()
    await session.init()

    len_chunk = 4  # 并发
    chunks = [indices[k: k + len_chunk] for k in range(0, len(indices), len_chunk)]
    for i, chunk in enumerate(chunks):
        cur_results = await asyncio.gather(
            *[parse_1_chapter_bodies(session, url, rule, class_body_page_loader)
              for url, chapter_name in chunk]
        )
        results += [(url, chapter_name, body_page_datas) for (url, chapter_name), body_page_datas in zip(chunk, cur_results)]
        logger.info(f'爬取正文第 {i} 轮次结束')
        if isinstance(session, playwright_websession.WebSession):
            logger.debug(f"本轮次结束一共有 {len(session.main_pages)} 个 Page，有 {len([value for value in session.main_pages.values() if not value])} 个锁定状态")

    await session.close()
    ###################################################################################################################################################

    # 存成书
    urls = []
    chapters_names = []
    content = []
    encodings = []
    for url, chapter_name, body_page_datas in results:
        urls.append(url)
        chapters_names.append(chapter_name)
        content.append([paragraph for body_page_data in body_page_datas for paragraph in body_page_data.content])
        logger.debug(f'本章节的起始页 url = {url}, encoding = {[body_page_data.raw_page_data.encoding for body_page_data in body_page_datas]}')
        assert len(set(body_page_data.raw_page_data.encoding for body_page_data in body_page_datas)) == 1
        encodings.append(body_page_datas[0].raw_page_data.encoding)

    book = Book(urls=urls,
                chapters_names=chapters_names,
                encodings=encodings,
                content=content
                )
    for i, chapter in enumerate(book.to_json()):
        utils.save_json(f'data/{i}.json',
                        {
                            'url': chapter['url'],
                            'title': chapter['chapter_name'],
                            'encoding': chapter['encoding'],
                            'content': chapter['content'],
                        })


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
