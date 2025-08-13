import os
import time
from datetime import datetime

from config.config import settings as config_file
from constants.notifications.common import TELEGRAM
from helpers.decorators import retry_on_exceptions
from helpers.logger import logger
from helpers.webdriver.find_element import find_element_by_xpath_and_click_it_with_javascript, \
    find_element_by_id_and_click_it_with_javascript, find_element
from helpers.webdriver.waits import wait_presence_of_element_located
from service.notifications_service import NotificationsService
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

        logger.info('Waiting 10 seconds to accept popup')
        time.sleep(10)
        self.driver.switch_to.alert.accept()

        logger.info('Waiting for appointments page to be fully loaded')
        wait_presence_of_element_located(self.driver, self.config.wait_timeout, 'ID', 'idCaptchaButton')
        find_element_by_id_and_click_it_with_javascript(self.driver, 'idCaptchaButton')

        wait_presence_of_element_located(self.driver, self.config.wait_timeout, 'ID', 'idListServices')
        logger.info('Checking if there\'s any available service')
        services_list = find_element(self.driver, 'ID', 'idListServices')
        # if not services_list.text:
        #     logger.info('No available appointments found')
        #     return

        logger.info('Apparently there are available services. Notifying on Telegram')
        # NotificationsService().post_notification(TELEGRAM, "@jerepfluger aparentemente hay turnos")
        # NotificationsService().post_notification(TELEGRAM, "@+34645692096 aparentemente hay turnos")
        # NotificationsService().post_notification(TELEGRAM, "@+376620214 aparentemente hay turnos")

        logger.info('Saving screenshot and html_source code')
        self.save_screenshot_and_html_source_code()

    def save_screenshot_and_html_source_code(self):
        debug_dir = ensure_debug_folder_exists()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        screenshot_path = os.path.join(debug_dir, f"page_screenshot_{timestamp}.png")
        self.driver.save_screenshot(screenshot_path)

        html_path = os.path.join(debug_dir, f"page_source_{timestamp}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

def ensure_debug_folder_exists():
    """
    Ensures a debug folder exists in the root directory and returns its path
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go one level up (parent directory)
    parent_dir = os.path.dirname(script_dir)

    # Create debug folder in the parent directory
    debug_dir = os.path.join(parent_dir, "debug")
    os.makedirs(debug_dir, exist_ok=True)

    return debug_dir
