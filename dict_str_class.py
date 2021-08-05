from loader.playwright_loaders import PlaywrightBodyPageLoader, PlaywrightIndexPageLoader
from loader.aiohttp_loaders import AiohttpBodyPageLoader, AiohttpIndexPageLoader
import playwright_websession
import aiohttp_websession
from parse_rule.aiohttp_low_rules import LxmlCssElementRule, BodyPageContentLxmlCssElementRule
from parse_rule.playwright_low_rules import PlaywrightElementRule, BodyPageContentPlaywrightElementRule, PlaywrightClickRule

body_page_loaders = {
    'playwright': PlaywrightBodyPageLoader,
    'aiohttp': AiohttpBodyPageLoader
}
index_page_loaders = {
    'playwright': PlaywrightIndexPageLoader,
    'aiohttp': AiohttpIndexPageLoader
}


web_sessions = {
    'playwright': playwright_websession.WebSession,
    'aiohttp': aiohttp_websession.WebSession
}


low_rules = {
    'LxmlCssElementRule': LxmlCssElementRule,
    'BodyPageContentLxmlCssElementRule': BodyPageContentLxmlCssElementRule,
    'PlaywrightElementRule': PlaywrightElementRule,
    'BodyPageContentPlaywrightElementRule': BodyPageContentPlaywrightElementRule,
    'PlaywrightClickRule': PlaywrightClickRule
}
