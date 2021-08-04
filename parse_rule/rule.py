"""
直接与 loader 进行交互，执导从 html 或 root 中提取数据
"""
import dict_str_class


class PageRule:
    """
    负责正文或目录的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了））
    """
    def __init__(self, page_rule: dict):
        """

        :param page_rule: 该页面所有的 rule
        """
        self.content_rules = [dict_str_class.low_rules[rule['type']](**rule['kwargs']) for rule in page_rule['content']]
        self.next_page_url_rules = [dict_str_class.low_rules[rule['type']](**rule['kwargs']) for rule in page_rule['next_page_url']]
        self.content_other_settings = page_rule.get('content_other_settings', {})


class BodyPageRule(PageRule):
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    """

    def __init__(self, body_page_rule: dict):
        """

        :param body_page_rule: 正文页面所有的 rule
        """
        super().__init__(body_page_rule)
        rule = body_page_rule['title']
        self.title_rule = dict_str_class.low_rules[rule['type']](**rule['kwargs'])


class IndexPageRule(PageRule):
    """
    负责目录页的某个 page
    """

    def __init__(self, index_page_rule: dict):
        """

        :param index_page_rule: 此网站所有的 rule（包括了网站设置、目录等等）
        """
        super().__init__(index_page_rule)


class WebsiteSettingRule:
    def __init__(self, all_rules_of_1_website: dict):
        """

        :param all_rules_of_1_website: 目录页面所有的 rule
        """
        self.encoding = all_rules_of_1_website.get('encoding', None)
        user_agent = ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like'
                      'Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko)'
                      'CriOS/65.0.3325.152 Mobile/15D100 Safari/604.1')
        self.headers = {'User-Agent': user_agent, **all_rules_of_1_website.get('headers', {})}


class WebsiteRule:
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    """
    def __init__(self, all_rules_of_1_website: dict):
        self.all_rules_of_1_website = all_rules_of_1_website
        self.body_page_rule = BodyPageRule(all_rules_of_1_website['body_page'])  # 正文 page 的规则定义（怎么获取下一章、怎么提取 title 等）
        self.index_page_rule = IndexPageRule(all_rules_of_1_website['index_page'])  # 目录 page 的规则定义（怎么获取每一章等）
        self.website_setting_rule = WebsiteSettingRule(all_rules_of_1_website)  # 整体网站的请求约束（UA、编码等）
