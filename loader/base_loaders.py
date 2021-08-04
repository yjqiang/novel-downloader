from typing import Any, Tuple
from urllib.parse import urljoin

from my_dataclass.body_page import BodyPageData
from my_dataclass.index_page import IndexPageData
from my_dataclass.content import ContentParagraph, ContentWords
from parse_rule.rule import BodyPageRule, IndexPageRule, WebsiteSettingRule
import utils


class IndexPageLoader:
    """
    负责正文的目录页（注意目录页也可能好几页）
    """
    @staticmethod
    async def fetch_html(session: Any, website_setting_rule: WebsiteSettingRule, index_page: IndexPageData) -> None:
        pass

    @staticmethod
    async def get_content(index_page_rule: IndexPageRule, index_page: IndexPageData) -> None:
        assert len(index_page_rule.content_rules) == 1
        content_rule = index_page_rule.content_rules[0]
        results: list[Tuple[str, str]] = await content_rule.findall_attr(index_page.raw_page_data)

        # https://stackoverflow.com/questions/8081545/how-to-convert-list-of-tuples-to-multiple-lists
        urls, chapters_names = list(zip(*results))

        index_page.urls = [urljoin(index_page.url, url) for url in urls]
        index_page.chapters_names = chapters_names

    @staticmethod
    async def get_next_page_url(index_page_rule: IndexPageRule, index_page: IndexPageData) -> None:
        pass

    @staticmethod
    async def goto_next_page(session: Any, website_setting_rule: WebsiteSettingRule, cur_index_page: IndexPageData) -> IndexPageData:
        """
        根据当前页的数据，获取下一页的真实 url 地址并加载
        :param session:
        :param website_setting_rule:
        :param cur_index_page:
        :return:
        """
        pass


class BodyPageLoader:
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    同步的（没有目录页），必须依次获得下一章
    """
    @staticmethod
    async def fetch_html(session: Any, website_setting_rule: WebsiteSettingRule, body_page: BodyPageData) -> None:
        pass

    @staticmethod
    async def get_title(body_page_rule: BodyPageRule, body_page: BodyPageData) -> None:
        title_rule = body_page_rule.title_rule
        title = await title_rule.find_attr(body_page.raw_page_data)
        assert len(title) == 1
        body_page.title = str(title[0]).strip()

    @staticmethod
    async def get_content(body_page_rule: BodyPageRule, body_page: BodyPageData) -> None:
        content_rules = body_page_rule.content_rules
        paragraphs: list[ContentParagraph] = []
        for content_rule in content_rules:
            # 其实这里默认了不能 regex（暂不支持）
            paragraphs += await content_rule.findall_attr(body_page.raw_page_data)

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
    async def get_next_page_url(body_page_rule: BodyPageRule, body_page: BodyPageData) -> None:
        pass

    @staticmethod
    async def goto_next_page(session: Any, website_setting_rule: WebsiteSettingRule, cur_body_page: BodyPageData) -> IndexPageData:
        """
        根据当前页的数据，获取下一页的真实 url 地址并加载
        :param session:
        :param website_setting_rule:
        :param cur_body_page:
        :return:
        """
        pass
