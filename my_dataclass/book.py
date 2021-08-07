from typing import Optional

from my_dataclass.content import ContentParagraph


class Book:
    def __init__(self, urls: Optional[list[str]] = None, chapters_names: Optional[list[str]] = None,
                 encodings: Optional[list[str]] = None, content: Optional[list[list[ContentParagraph]]] = None):

        # 每个 chapter 可能有好几个 BodyPageData（每章有好几页正文）
        # [[url, chapter_name, [正文]], ...]

        if urls is None:
            urls = list()
        if chapters_names is None:
            chapters_names = list()
        if encodings is None:
            encodings = list()
        if content is None:
            content = list()
        self.urls: list[str] = urls
        self.chapters_names: list[str] = chapters_names
        self.content: list[list[ContentParagraph]] = content  # list[第一章的所有自然段，第二章的所有自然段...]
        self.encodings: list[str] = encodings

    def append(self, url: str, chapter_name: str, paragraphs: list[ContentParagraph], encoding: str):
        """
        输入某一章的目录、章节名、所有自然段
        :param encoding:
        :param url:
        :param chapter_name:
        :param paragraphs:
        :return:
        """
        self.urls.append(url)
        self.chapters_names.append(chapter_name)
        self.content.append(paragraphs)
        self.encodings.append(encoding)

    def to_json(self) -> list[dict]:
        """

        :return: list 的每个元素就是某一章
        """
        return [
            {
                'url': url,
                'chapter_name': chapter_name,
                'encoding': encoding,
                'content': [paragraph.to_json() for paragraph in paragraphs],
            }
            for url, chapter_name, paragraphs, encoding in zip(self.urls, self.chapters_names, self.content, self.encodings)
        ]

    @staticmethod
    def from_json(json_data: list[dict]) -> 'Book':
        urls = []
        chapters_names = []
        encodings = []
        content = []

        for element in json_data:
            urls.append(element['url'])
            chapters_names.append(element['chapter_name'])
            encodings.append(element['encoding'])
            content.append([ContentParagraph.from_json(paragraph) for paragraph in element['content']])

        return Book(urls=urls, chapters_names=chapters_names, encodings=encodings, content=content)





