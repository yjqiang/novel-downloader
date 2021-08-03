import sys
import asyncio
from typing import Optional, Tuple

import aiohttp


class WebSession:
    __slots__ = ('session',)

    def __init__(self):
        self.session = None

    async def init(self) -> None:
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))

    @staticmethod
    async def _recv_str(rsp: aiohttp.ClientResponse, encoding: Optional[str] = None) -> Tuple[str, str]:
        return await rsp.text(encoding=encoding), encoding or rsp.get_encoding()

    # 基本就是通用的 request
    async def _orig_req(self, parse_rsp, method: str, url: str, encoding: Optional[str] = None, **kwargs):
        i = 0
        while True:
            i += 1
            if i >= 5:
                print(f'反复请求多次未成功, {url}, {kwargs}')
                await asyncio.sleep(1)
            try:
                async with self.session.request(method, url, **kwargs) as rsp:
                    print(f'{url=}, {rsp.status=}, {kwargs=}, {rsp.url=}')
                    if rsp.status == 200:
                        return await parse_rsp(rsp, encoding)
                    else:
                        print(f'STATUS_CODE ERROR: {url} {rsp.status} {await self._recv_str(rsp)} {kwargs}')
                        print("FATAL ERROR")
                        sys.exit(-1)
            except Exception as e:
                # print('当前网络不好，正在重试，请反馈开发者!!!!')
                print(e, sys.exc_info()[0], sys.exc_info()[1], url)

    async def request_text(self,
                           method: str,
                           url: str,
                           encoding: Optional[str] = None,
                           **kwargs) -> Tuple[str, str]:
        return await self._orig_req(self._recv_str, method, url, encoding, **kwargs)

    async def close(self) -> None:
        await self.session.close()

    def set_state(self, *_, **__) -> None:
        pass
