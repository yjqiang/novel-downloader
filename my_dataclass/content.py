from typing import Union

from lxml import etree


class ContentWords:
    """
    一部分话
    """
    def __init__(self, words: str):
        self.words = words

    def __str__(self) -> str:
        return self.words

    def to_json(self) -> dict:
        return {
            'type': 'Words',
            'data': {
                'words': self.words
            }
        }

    def to_html(self) -> etree._Element:
        root = etree.Element("div")
        root.text = self.words
        return root


class ContentImage:
    """
    图文字
    """

    def __init__(self, url: str):
        self.url = url

    def __str__(self) -> str:
        return f'<img src="{self.url}">'

    def to_json(self) -> dict[str, str]:
        return {
            'type': 'Image',
            'data': {
                'url': self.url
            }
        }

    def to_html(self) -> etree._Element:
        root = etree.Element("img")
        root.set('src', self.url)
        return root


class ContentParagraph:
    """
    用在正文就是一个自然段；在目录就是一个章节的名字，防止正文里面有文字图
    """
    DICT_TYPE_CLASS = {
        'Words': ContentWords,
        'Image': ContentImage
    }

    def __init__(self, value: list[Union[ContentWords, ContentImage]]):
        self.value: list[Union[ContentWords, ContentImage]] = value

    def __str__(self) -> str:
        return ''.join(str(element) for element in self.value)

    def to_json(self) -> list[dict]:
        return [element.to_json() for element in self.value]

    def to_html(self) -> etree._Element:
        root = etree.Element("p")
        root.text = '　　'
        last_tag = root  # 存放 text
        for i, piece in enumerate(self.value):
            if isinstance(piece, ContentWords):
                if last_tag == root:
                    root.text += piece.words
                else:
                    assert last_tag.tag == 'img'
                    last_tag.tail = piece.words
            else:
                last_tag = piece.to_html()
                root.append(last_tag)
        return root

    @staticmethod
    def from_json(json_data: list[dict]) -> 'ContentParagraph':
        return ContentParagraph([ContentParagraph.DICT_TYPE_CLASS[element['type']](**element['data']) for element in json_data])
