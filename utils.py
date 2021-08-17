import json
import re
from typing import Any

from lxml.etree import _Element

import toml
import opencc


RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
T2S_CONVERTER = opencc.OpenCC('t2s.json')


def is_fake_paragraph(last_word: str):
    """
    不少小说网站乱切分自然段，这里根据每个“自然段”最后一个 word 尝试进行合并
    本函数负责判定是否真的自然段结尾
    :param last_word:
    :return:
    """
    # https://stackoverflow.com/questions/2718196/find-all-chinese-text-in-a-string-using-python-and-regex
    return RE.fullmatch(last_word) or last_word in (',', '，', '、')


def save_json(path: str, data: Any, encoding: str = 'utf-8') -> None:
    with open(path, 'w+', encoding=encoding) as f:
        f.write(json.dumps(data, indent=4))


def open_json(path: str, encoding: str = 'utf-8') -> Any:
    with open(path, encoding=encoding) as f:
        return json.load(f)


def toml_load(path: str, encoding: str = 'utf-8'):
    with open(path, encoding=encoding) as f:
        return toml.load(f)


def toml_dump(anything: Any, path: str, encoding: str = 'utf-8') -> None:
    with open(path, 'w', encoding=encoding) as f:
        toml.dump(anything, f)


def traditional2simplified_chinese(words: str) -> str:
    return T2S_CONVERTER.convert(words)


etree_Element = _Element  # 这货是非 public 的，不知道 lxml 咋整的。。。
