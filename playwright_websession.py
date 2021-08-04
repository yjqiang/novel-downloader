# from logging import info as print
import logging
from typing import Tuple, Optional, Union

# from lxml import cssselect, etree, html
from playwright.async_api import async_playwright, Page, ElementHandle

import log

log.init()


class WebSession:
    __slots__ = ('main_pages', 'context', 'browser',)

    def __init__(self):
        self.main_pages: dict[Page, bool] = {}  # True 表示完事了
        self.context = None
        self.browser = None

    async def init(self):
        self.browser = await (await async_playwright().start()).chromium.launch(channel="chrome", headless=True)
        self.context = await self.browser.new_context()

    async def request_text(self, url: Union[str, ElementHandle], page: Optional[Page] = None) -> Tuple[Page, str]:
        """

        :param page:
        :param url: url 为 ElementHandle 时，点击进入页面；为 str，goto 进入页面
        :return: page 和 网页编码
        """

        if isinstance(url, str):
            for key, value in self.main_pages.items():
                if value:
                    page = key  # 复用
                    break
            else:
                page = await self.context.new_page()

            self.main_pages[page] = False  # 在占用
            await page.goto(url)
        else:
            assert page is not None
            async with page.expect_navigation():
                await url.click()

        # 想 wait until page **稳定**下来，然后提取最终的 html
        logging.info("START")
        last_html = '-1'
        while True:
            # # https://github.com/microsoft/playwright/issues/1115#issuecomment-791122240
            # for _ in range(20):
            #     await page.keyboard.press("PageDown")

            # https://github.com/microsoft/playwright/issues/4302
            await page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
            cur_html = await page.evaluate(
                """
                const waitAndGetHtml = delay => new Promise(
                    resolve => setTimeout(
                        () => resolve(document.documentElement.outerHTML),
                        delay)
                );
                const test = async () => {
                    let last_html = document.documentElement.outerHTML;
                    let cur_html;
                    while (true) {
                        cur_html = await waitAndGetHtml(500);
                        if (last_html === cur_html)
                            return cur_html;
                        last_html = cur_html;
                    }
                }
                test();
                """
            )
            if last_html == cur_html:
                break
            last_html = cur_html
        logging.info("DOWN")
        # # 不知道为什么，page.query_selector_all 和 lxml 解析 content 结果几乎完全没关系
        # print(len(await page.query_selector_all('div[id=content] > div > p')))
        # root = html.fromstring(await page.evaluate('() => document.documentElement.outerHTML'), parser=etree.HTMLParser(encoding='utf-8', remove_comments=True))
        # result = cssselect.CSSSelector('div[id=content] > div > p')(root)
        # for i in result:
        #     print(etree.tostring(i))
        # print(len(result))

        return page, await page.evaluate("() => document.characterSet")

    async def close(self) -> None:
        await self.browser.close()

    def set_state(self, page: Page, value: bool) -> None:
        self.main_pages[page] = value
