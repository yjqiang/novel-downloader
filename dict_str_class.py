from loader.playwright_loaders import PlaywrightBodyPageLoader
from loader.aiohttp_loaders import AiohttpBodyPageLoader
import playwright_websession
import aiohttp_websession
from parse_rule.aiohttp_low_rules import AiohttpLxmlHtmlElementRule, BodyPageContentAiohttpLxmlHtmlElementRule
from parse_rule.playwright_low_rules import PlaywrightLxmlHtmlElementRule, BodyPageContentPlaywrightLxmlHtmlElementRule


body_page_loaders = {
    'playwright': PlaywrightBodyPageLoader,
    'aiohttp': AiohttpBodyPageLoader
}


web_sessions = {
    'playwright': playwright_websession.WebSession,
    'aiohttp': aiohttp_websession.WebSession
}


low_rules = {
    'AiohttpLxmlHtmlElementRule': AiohttpLxmlHtmlElementRule,
    'BodyPageContentAiohttpLxmlHtmlElementRule': BodyPageContentAiohttpLxmlHtmlElementRule,
    'PlaywrightLxmlHtmlElementRule': PlaywrightLxmlHtmlElementRule,
    'BodyPageContentPlaywrightLxmlHtmlElementRule': BodyPageContentPlaywrightLxmlHtmlElementRule
}
