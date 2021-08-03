from typing import Any
from urllib.parse import urljoin

from my_dataclass.body_page import BodyPage
from my_dataclass.content import ContentParagraph, ContentWords
from parse_rule.rule import BodyPageRule, WebsiteSettingRule
import utils


class BodyPageLoader:
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    同步的（没有目录页），必须依次获得下一章
    """

    @staticmethod
    async def get_title(body_page_rule: BodyPageRule, body_page: BodyPage) -> None:
        title_rule = body_page_rule.title_rule
        title = await title_rule.find_attr(body_page.web_content)
        assert len(title) == 1
        body_page.title = str(title[0]).strip()

    @staticmethod
    async def get_content(body_page_rule: BodyPageRule, body_page: BodyPage) -> None:
        content_rules = body_page_rule.content_rules
        paragraphs: list[ContentParagraph] = []
        for content_rule in content_rules:
            # 其实这里默认了不能 regex（暂不支持）
            paragraphs += await content_rule.findall_attr(body_page.web_content)

        if body_page_rule.content_other_settings.get('try_combine_fake_paragraphs', False):
            for i in range(len(paragraphs) - 2, -1, -1):
                # https://stackoverflow.com/questions/43637799/how-to-combine-two-elements-of-a-list-based-on-a-given-condition-in-python
                cur_last_piece = paragraphs[i].value[-1]  # 本自然段的最后部分

                if isinstance(cur_last_piece, ContentWords) and utils.is_fake_paragraph(cur_last_piece.words[-1]):
                    after_first_piece = paragraphs[i + 1].value[0]  # 后一个自然段的第一部分
                    if isinstance(after_first_piece, ContentWords):  # 合并连在一起的 string
                        paragraphs[i].value[-1].words = cur_last_piece.words + after_first_piece.words
                        paragraphs[i].value += paragraphs[i + 1].value[1:]
                    else:
                        paragraphs[i].value += paragraphs[i + 1].value

                    paragraphs.pop(i + 1)
        body_page.content = paragraphs

    @staticmethod
    async def get_next_page_url(body_page_rule: BodyPageRule, body_page: BodyPage) -> None:
        next_page_url_rules = body_page_rule.next_page_url_rules
        for next_page_url_rule in next_page_url_rules:
            result = await next_page_url_rule.find_attr(body_page.web_content)
            if result is not None:
                link = result[0]
                body_page.next_page_url = urljoin(body_page.url, link)
                return

    @staticmethod
    async def fetch_html(session: Any, website_setting_rule: WebsiteSettingRule, body_page: BodyPage) -> None:
        pass
