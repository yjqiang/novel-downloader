from copy import copy

from lxml import etree, html, cssselect
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

import utils
from my_dataclass.content import ContentParagraph

APP = FastAPI()
with open('conf/test.html', encoding='utf-8') as f:
    TREE = html.fromstring(f.read(), parser=etree.HTMLParser(remove_comments=True))


@APP.get("/{item_id}.html", response_class=HTMLResponse)
def sync_sleep(item_id: str):
    tree = copy(TREE)
    data = utils.open_json(f'data/{item_id}.json')

    node = cssselect.CSSSelector('meta')(tree)[0]
    node.set('charset', data['encoding'])

    node = cssselect.CSSSelector('title')(tree)[0]
    node.text = data['title']

    # 正文
    node = cssselect.CSSSelector('article')(tree)[0]
    for paragraph in data['content']:
        content_paragraph = ContentParagraph.from_json(paragraph)
        node.append(content_paragraph.to_html())

    # 下一页设置
    node = cssselect.CSSSelector('div > ul > li > a')(tree)[0]
    node.set('href', f'{int(item_id) + 1}.html')

    return html.tostring(tree).decode()


@APP.get("/")
async def home():
    response = RedirectResponse(url='/0.html')
    return response


if __name__ == "__main__":
    uvicorn.run('main_reader:APP', host="127.0.0.1", port=8000)
