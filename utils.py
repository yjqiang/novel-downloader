import json
import re
from typing import Any

import toml


RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)


def is_fake_paragraph(last_word: str):
    """
    不少小说网站乱切分自然段，这里根据每个“自然段”最后一个 word 尝试进行合并
    本函数负责判定是否真的自然段结尾
    :param last_word:
    :return:
    """
    # https://stackoverflow.com/questions/2718196/find-all-chinese-text-in-a-string-using-python-and-regex
    return RE.fullmatch(last_word) or last_word in (',', '，', '、')


def save_json(path: str, data: Any) -> None:
    with open(path, 'w+', encoding='utf8') as f:
        f.write(json.dumps(data, indent=4))


def open_json(path: str) -> Any:
    with open(path, encoding='utf8') as f:
        return json.load(f)


def toml_load(path: str):
    with open(path, encoding="utf-8") as f:
        return toml.load(f)


def toml_dump(anything: Any, path):
    with open(path, 'w', encoding="utf-8") as f:
        toml.dump(anything, f)
