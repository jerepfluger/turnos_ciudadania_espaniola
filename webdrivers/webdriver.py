from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver as wirewebdriver
# A package to have a chromedriver always up-to-date.
from webdriver_manager.chrome import ChromeDriverManager

from config.config import settings
from helpers.logger import logger
from helpers.webdriver.config_helper import retrieve_firefox_binary_path_based_on_os, \
    retrieve_chrome_binary_path_based_on_os


class ChromeWebdriver:
    @staticmethod
    def create(user_agent=None, proxy=None, use_profile=False, browser_name='chromium'):
        logger.info(f'Creating {browser_name} Web Driver')
        options = ChromeOptions()
        options.binary_location = retrieve_chrome_binary_path_based_on_os(settings.web_driver.chrome_binary,
                                                                          browser_name)
        options.add_argument('headless')
        # options.add_argument("--incognito")  # Launches browser in incognito mode
        options.add_argument('--hide-scrollbars')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu')
        # options.add_argument('--no-sandbox')
        options.add_argument('--data-path={}'.format(settings.web_driver.chromium.data_path))
        options.add_argument('--disk-cache-dir={}'.format(settings.web_driver.chromium.cache_dir))
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-autofill")
        options.add_argument("--disable-password-manager")
        options.add_argument("--ignore-certificate-errors")
        if user_agent:
            options.add_argument(f'--user-agent={user_agent}')
        # Disable web security for get ember components via execute-scripts
        options.add_argument('disable-web-security')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-geolocation")

        # Use current profile
        if use_profile:
            options.add_argument(
                "--user-data-dir=/Users/jeremiaspfluger/Library/Application Support/Google/Chrome_Selenium")
            options.add_argument("--profile-directory=Default")  # Change if needed

        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        desired_capabilities = webdriver.DesiredCapabilities.CHROME
        # This flag is supposed to help pages to load complete on slow traffic site without breaking
        desired_capabilities['pageLoadStrategy'] = 'normal'

        if proxy:
            options.add_argument('proxy-server={}:{}'.format(proxy.host, proxy.port))

        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(desired_capabilities=desired_capabilities, chrome_options=options)
        driver.set_page_load_timeout(10)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver


class FirefoxWebdriver:
    @staticmethod
    def create(user_agent=None, proxy=None, use_profile=False):
        proxy = proxy
        logger.info('Creating Firefox Web Driver')
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.disable_open_during_load", True)
        profile.set_preference("dom.webnotifications.enabled", False)
        profile.set_preference("signon.autofillForms", False)
        profile.set_preference("signon.rememberSignons", False)
        profile.set_preference("permissions.default.image", 2)
        profile.set_preference("webdriver_accept_untrusted_certs", True)
        profile.set_preference("webdriver_assume_untrusted_issuer", True)

        if user_agent:
            profile.set_preference("general.useragent.override", user_agent)

        options = FirefoxOptions()
        options.binary_location = retrieve_firefox_binary_path_based_on_os(settings.web_driver.firefox_binary)
        options.add_argument('--headless')
        # options.add_argument("-private")  # Firefox incognito mode
        options.add_argument('--new_instance')
        for item in settings.web_driver.firefox.options:
            options.set_preference(item, settings.web_driver.firefox.options[item])
        desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
        # This flag is supposed to help pages to load complete on slow traffic site without breaking
        desired_capabilities['pageLoadStrategy'] = 'normal'

        # Proxy
        if proxy:
            logger.info('Setting proxy values to http {} and port {}'.format(proxy.host, proxy.port))
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", proxy.host)
            options.set_preference("network.proxy.http_port", proxy.port)
            options.set_preference("network.proxy.share_proxy_settings", True)
            options.set_preference("network.proxy.ssl", proxy.host)
            options.set_preference("network.proxy.ssl_port", proxy.port)

        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(10)

        return driver


class WebDriver:
    def __init__(self):
        self.web_driver_creators = {'firefox': FirefoxWebdriver.create, 'chromium': ChromeWebdriver.create,
                                    'chrome': ChromeWebdriver.create}

    def acquire(self, webdriver_type, user_agent=None, proxy=None, use_profile=False):
        if webdriver_type in self.web_driver_creators:
            if webdriver_type == 'chrome' or webdriver_type == 'chromium':
                return self.web_driver_creators[webdriver_type](user_agent=user_agent, proxy=proxy,
                                                                use_profile=use_profile, browser_name='chrome')

            return self.web_driver_creators[webdriver_type](user_agent, proxy, use_profile)

        return None
