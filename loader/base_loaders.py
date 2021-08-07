from typing import Any, Tuple
from urllib.parse import urljoin

from my_dataclass.body_page import BodyPageData
from my_dataclass.index_page import IndexPageData
from my_dataclass.content import ContentParagraph, ContentWords, ContentImage
from parse_rule.rule import BodyPageRule, IndexPageRule, WebsiteSettingRule
import utils


class IndexPageLoader:
    """
    负责正文的目录页（注意目录页也可能好几页）
    """
    @staticmethod
    async def fetch_html(session: Any, website_setting_rule: WebsiteSettingRule, page_data: IndexPageData) -> None:
        pass

    @staticmethod
    async def get_content(page_rule: IndexPageRule, page_data: IndexPageData) -> None:
        assert len(page_rule.content_rules) == 1
        content_rule = page_rule.content_rules[0]
        results: list[Tuple[str, str]] = await content_rule.findall_attr(page_data.raw_page_data)

        # https://stackoverflow.com/questions/8081545/how-to-convert-list-of-tuples-to-multiple-lists
        urls, chapters_names = list(zip(*results))

        page_data.urls = [urljoin(page_data.url, url) for url in urls]
        page_data.chapters_names = chapters_names

    @staticmethod
    async def get_next_page_url(page_rule: IndexPageRule, page_data: IndexPageData) -> None:
        pass

    @staticmethod
    async def goto_next_page(session: Any, website_setting_rule: WebsiteSettingRule, cur_page_data: IndexPageData) -> IndexPageData:
        """
        根据当前页的数据，获取下一页的真实 url 地址并加载
        :param session:
        :param website_setting_rule:
        :param cur_page_data:
        :return:
        """
        pass


class BodyPageLoader:
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    同步的（没有目录页），必须依次获得下一章
    """
    @staticmethod
    async def fetch_html(session: Any, website_setting_rule: WebsiteSettingRule, page_data: BodyPageData) -> None:
        pass

    @staticmethod
    async def get_title(page_rule: BodyPageRule, page_data: BodyPageData) -> None:
        title_rule = page_rule.title_rule
        title = await title_rule.find_attr(page_data.raw_page_data)
        assert len(title) == 1
        page_data.title = str(title[0]).strip()

    @staticmethod
    async def get_content(page_rule: BodyPageRule, page_data: BodyPageData) -> None:
        content_rules = page_rule.content_rules
        paragraphs: list[ContentParagraph] = []
        for content_rule in content_rules:
            # 其实这里默认了不能 regex（暂不支持）
            paragraphs += await content_rule.findall_attr(page_data.raw_page_data)

        if page_rule.content_other_settings.get('try_combine_fake_paragraphs', False):
            for i in range(len(paragraphs) - 2, -1, -1):
                # https://stackoverflow.com/questions/43637799/how-to-combine-two-elements-of-a-list-based-on-a-given-condition-in-python
                cur_last_piece = paragraphs[i].value[-1]  # 本自然段的最后部分

                if isinstance(cur_last_piece, ContentWords) and utils.is_fake_paragraph(cur_last_piece.words[-1]):
                    after_first_piece = paragraphs[i + 1].value[0]  # 后一个自然段的第一部分
                    if isinstance(after_first_piece, ContentWords):  # 合并连在一起的 string：把后一个自然段的第一部分（全是 str）附在本段的最后部分末尾，并删除后一个自然段的第一部分
                        paragraphs[i].value[-1].words = cur_last_piece.words + after_first_piece.words
                        paragraphs[i].value += paragraphs[i + 1].value[1:]
                    else:  # 仅仅简单的合并两自然段
                        paragraphs[i].value += paragraphs[i + 1].value

                    paragraphs.pop(i + 1)
                elif isinstance(cur_last_piece, ContentImage):  # 这里假设文字图不含标点符号
                    # 仅仅简单的合并两自然段
                    paragraphs[i].value += paragraphs[i + 1].value
                    paragraphs.pop(i + 1)

        if page_rule.content_other_settings.get('traditional2simplified_chinese', False):
            for paragraph in paragraphs:
                for piece in paragraph.value:
                    if isinstance(piece, ContentWords):
                        piece.words = utils.traditional2simplified_chinese(piece.words)

        page_data.content = paragraphs

    @staticmethod
    async def get_next_page_url(page_rule: BodyPageRule, page_data: BodyPageData) -> None:
        pass

    @staticmethod
    async def goto_next_page(session: Any, website_setting_rule: WebsiteSettingRule, cur_page_data: BodyPageData) -> BodyPageData:
        """
        根据当前页的数据，获取下一页的真实 url 地址并加载
        :param session:
        :param website_setting_rule:
        :param cur_page_data:
        :return:
        """
        pass
