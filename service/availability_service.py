import time

from config.config import settings as config_file
from helpers.decorators import retry_on_exceptions
from helpers.logger import logger
from helpers.webdriver.find_element import find_element_by_xpath_and_click_it_with_javascript, \
    find_element_by_id_and_click_it_with_javascript, find_element
from helpers.webdriver.waits import wait_presence_of_element_located
from webdrivers.webdriver import WebDriver


class SpanishCitizenshipService:
    def __init__(self):
        self.config = config_file.spanish_citizenship_service
        self.driver = None

    @retry_on_exceptions(
        exceptions=[Exception],
        delay=5,
        max_retries=10,
        before_retry="close_driver"
    )
    def check_appointment_availability(self):
        logger.info('Starting availability check process')
        self.start_webdriver()

        self.check_availability()

    def start_webdriver(self):
        self.driver = WebDriver().acquire(self.config.browser_type)

    def check_availability(self):
        logger.info('Navigating to embassy webpage')
        self.driver.get(self.config.base_url)
        wait_presence_of_element_located(self.driver, self.config.wait_timeout, 'ID', 'DeltaSPWebPartManager')

        logger.info('Page loaded. Click on AQUI button to check availability process')
        find_element_by_xpath_and_click_it_with_javascript(self.driver, './/*[contains(text(), "AQUÍ")]')

        logger.info('Waiting 3 seconds to accept popup')
        time.sleep(3)
        self.driver.switch_to.alert.accept()

        logger.info('Waiting for appointments page to be fully loaded')
        wait_presence_of_element_located(self.driver, self.config.wait_timeout, 'ID', 'idCaptchaButton')
        find_element_by_id_and_click_it_with_javascript(self.driver, 'idCaptchaButton')

        wait_presence_of_element_located(self.driver, self.config.wait_timeout, 'ID', 'idListServices')
        logger.info('Checking if there\'s any available service')
        services_list = find_element(self.driver, 'ID', 'idListServices')
        if not services_list.text:
            return

        logger.info('Apparently there are available services. Notifying on Telegram')


    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
