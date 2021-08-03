"""
直接与 loader 进行交互，执导从 html 或 root 中提取数据
"""
import dict_str_class


class BodyPageRule:
    """
    负责正文的某个 page（例如某一章，或者某一章的某一页（有的网站把每一章节又细分了）），每个 page 对应一个 url
    """

    def __init__(self, all_rules_of_1_website: dict):
        """

        :param all_rules_of_1_website: 此网站所有的 rule（包括了正文、网站设置、目录等等）
        """
        rule = all_rules_of_1_website['title']
        self.title_rule = dict_str_class.low_rules[rule['type']](**rule['kwargs'])

        self.content_rules = [dict_str_class.low_rules[rule['type']](**rule['kwargs']) for rule in all_rules_of_1_website['content']]
        self.next_page_url_rules = [dict_str_class.low_rules[rule['type']](**rule['kwargs']) for rule in all_rules_of_1_website['next_page_url']]
        self.content_other_settings = all_rules_of_1_website.get('content_other_settings', {})


class WebsiteSettingRule:
    def __init__(self, all_rules_of_1_website: dict):
        """

        :param all_rules_of_1_website: 此网站所有的 rule（包括了正文、网站设置、目录等等）
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
        self.website_setting_rule = WebsiteSettingRule(all_rules_of_1_website)  # 整体网站的请求约束（UA、编码等）
