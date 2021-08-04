**本仓库 DEMO 等可能含有部分 NSFW 内容，请选择合适场合使用或查看**

# 介绍
1. **盗版小说网站**的质量参差不齐，格式排版贼烂，本仓库基于这样的问题，希望可以下载资源后，本地统一处理。
2. 本仓库借助强大的 [lxml](https://lxml.de/)，除了常见的纯文本的小说网站，同时还可以**兼容插有文字图**（用某个字的图片代替该文字）的网站。
3. 本仓库借助强大的 [playwright](https://playwright.dev/)，可以执行较为复杂的操作，例如可以**兼容下一页的跳转链接不是直接 URL** 时的场景（点击该元素即可，但是纯粹的 lxml 是难以做到的）。
4. **虽然是真的虚伪，但是我还是要说，支持正版，人人有责**。

# 使用说明
1. 请使用 **python 3.9+** 版本。
2. 依赖包在 [requirements.txt](requirements.txt)，使用 `pip install Package_name==version` 命令（例如 `pip install lxml==4.6.3`）安装即可。
3. [main_crawler.py](main_crawler.py) 负责下载小说到本地。
4. [main_reader.py](main_reader.py) 负责把本地小说展示出来（用网页浏览）。
5. [conf/rule.toml](conf/rule.toml) 负责小说提取规则。