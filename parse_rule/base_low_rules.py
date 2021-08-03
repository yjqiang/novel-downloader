from typing import Optional, Any, Union

from lxml import html

from my_dataclass.body_page import WebContent
from my_dataclass.content import ContentParagraph, ContentWords, ContentImage


class LxmlHtmlElementRule:
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        """

        :param str_pattern:
        :param attributes: [[function_name, *kwargs_except_root], ...]
        """
        self.str_pattern = str_pattern
        self.attributes = [[getattr(self, function_name), *kwargs_except_root] for function_name, *kwargs_except_root in attributes]

    @staticmethod
    async def _get_attribute(root: html.HtmlElement, key: str) -> str:
        return root.get(key)

    @staticmethod
    async def _get_text(root: html.HtmlElement) -> str:
        return root.text

    async def find(self, web_content: WebContent) -> Optional[html.HtmlElement]:
        pass

    async def findall(self, web_content: WebContent) -> list[html.HtmlElement]:
        pass

    async def find_attr(self, web_content: WebContent) -> Optional[list[Any]]:
        """
        self.attributes 设计目的：例如在目录页获取每个 index 的信息（url + 章节名），一般对同一个 element，element.get('href') 是 url，而 element.text 是章节名
        :param web_content:
        :return:
        """
        find_result = await self.find(web_content)
        if find_result is None:
            return None
        return [await function(find_result, *kwargs_except_root) for function, *kwargs_except_root in self.attributes]

    async def findall_attr(self, web_content: WebContent) -> list[list[Any]]:
        find_results = await self.findall(web_content)
        results = []
        for find_result in find_results:
            results.append([await function(find_result, *kwargs_except_root) for function, *kwargs_except_root in self.attributes])
        return results


class BodyPageContentLxmlHtmlElementRule:
    """
    正文提取的关键在于把所有的 tag 的 text 全部提取出来
    """
    def __init__(self, str_pattern: str, attributes: list[list[str]]):
        """

        :param str_pattern:
        :param attributes: [[function_name, *kwargs_except_root], ...]
        """
        self.str_pattern = str_pattern
        self.attributes = [[getattr(self, function_name), *kwargs_except_root] for function_name, *kwargs_except_root in attributes]

    @staticmethod
    async def _get_content(root: html.HtmlElement) -> list[ContentParagraph]:
        """
        br 会负责把各个自然段分割
        :param root:
        :return:
        """
        result = [root.text]
        for i in root.iterchildren():
            if i.tag == 'br':
                result.append('\n')
            result.append(i.text)
            result.append(i.tail)
        paragraphs = ''.join(i for i in result if i is not None)

        # 清理空白段落等
        result = []
        for paragraph in paragraphs.split('\n'):
            paragraph = paragraph.strip()
            if paragraph:
                result.append(ContentParagraph([ContentWords(paragraph)]))
        return result

    @staticmethod
    async def _get_content_with_img(root: html.HtmlElement, tag_name: str, attr_name: str) -> list[ContentParagraph]:
        """
        eg: http://m.haohengwx.com/16/16248/236927_3.html 有文字图
        br 会负责把各个自然段分割
        :param root:
        :return:
        """
        result = [root.text]
        for i in root.iterchildren():
            if i.tag == 'br':
                result.append('\n')
            elif i.tag == tag_name:
                result.append(ContentImage(i.get(attr_name)))  # 碰到 img 这种，把整个元素保存下来
            result.append(i.text)
            result.append(i.tail)

        result = [i for i in result if i is not None]

        paragraphs = []
        paragraph = []
        result.append('\n')  # 加一个结尾符号
        for element in result:
            assert isinstance(element, (str, ContentImage))
            if element == '\n':
                paragraphs.append(paragraph)
                paragraph = []
            else:
                paragraph.append(element)

        # 合并临近的字符串，这样操作后，每个 paragraph 就变成了 ['abcd\nefg', ContentImage(url), '\n', ContentImage(url), ...]；保证不会有 str 相连
        for paragraph in paragraphs:  # type: list[Union[ContentImage, str]]
            for i in range(len(paragraph) - 2, -1, -1):
                # https://stackoverflow.com/questions/43637799/how-to-combine-two-elements-of-a-list-based-on-a-given-condition-in-python
                cur, after = paragraph[i], paragraph[i + 1]
                if isinstance(cur, str) and isinstance(after, str):
                    paragraph[i] = cur + after
                    paragraph.pop(i + 1)  # 把后一个一个弹出来，由于后面的元素已经遍历了，所以不会影响之后的遍历

        # 删除句首句尾的空白
        new_paragraphs = []
        for paragraph in paragraphs:  # type: list[Union[ContentImage, str]]
            if paragraph:
                first = paragraph[0]
                if isinstance(first, str):
                    paragraph[0] = first.lstrip()
                    if not paragraph[0]:  # 前部分 str 全是空白
                        paragraph = paragraph[1:]

            if paragraph:
                last = paragraph[-1]
                if isinstance(last, str):
                    paragraph[-1] = last.rstrip()
                    if not paragraph[-1]:  # 后部分 str 全是空白
                        paragraph = paragraph[:-1]

            # str 处理为 ContentWords
            if paragraph:
                new_paragraph = []
                for piece in paragraph:
                    if isinstance(piece, str):
                        new_paragraph.append(ContentWords(piece))
                    else:
                        new_paragraph.append(piece)
                new_paragraphs.append(ContentParagraph(new_paragraph))

        return new_paragraphs

    async def findall(self, web_content: WebContent) -> list[html.HtmlElement]:
        pass

    async def findall_attr(self, web_content: WebContent) -> list[ContentParagraph]:
        find_results = await self.findall(web_content)
        paragraphs = []
        for find_result in find_results:
            for function, *kwargs_except_root in self.attributes:
                paragraphs += await function(find_result, *kwargs_except_root)

        return paragraphs
