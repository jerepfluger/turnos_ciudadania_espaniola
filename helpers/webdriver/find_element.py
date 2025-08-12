import random
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def find_elements(driver, selector_type, element_identifier):
    selector_type = selector_type.upper()
    if selector_type == 'ID':
        return driver.find_elements(By.ID, element_identifier)
    if selector_type == 'XPATH':
        return driver.find_elements(By.XPATH, element_identifier)

    raise NotImplementedError(f'No FindElementsBy implementation for selector_type: {selector_type}')


def find_element(driver, selector_type, element_identifier):
    selector_type = selector_type.upper()
    if selector_type == 'ID':
        return driver.find_element(By.ID, element_identifier)
    if selector_type == 'XPATH':
        return driver.find_element(By.XPATH, element_identifier)

    raise NotImplementedError(f'No FindElementBy implementation for selector_type: {selector_type}')


def find_element_and_click_it_with_javascript(driver, selector_type, element_identifier):
    element = find_element(driver, selector_type, element_identifier)
    _gradually_scroll_element_into_view(driver, element)

    # Click element with javascript
    driver.execute_script('arguments[0].click();', element)


def find_selector_element_and_select_option_with_text(driver, selector_type, element_identifier, text_identifier):
    element = find_element(driver, selector_type, element_identifier)
    _gradually_scroll_element_into_view(driver, element)

    procedure_selector = Select(element)
    if procedure_selector.first_selected_option.text != text_identifier:
        procedure_selector.select_by_visible_text(text_identifier)


def find_element_by_id_and_send_keys(driver, element_identifier, keys):
    _find_element_and_send_keys(driver, By.ID, element_identifier, keys)


def find_element_by_xpath_and_send_keys(driver, element_identifier, keys):
    _find_element_and_send_keys(driver, By.XPATH, element_identifier, keys)


def _find_element_and_send_keys(driver, selector_type, element_identifier, keys):
    element = driver.find_element(selector_type, element_identifier)
    element.location_once_scrolled_into_view

    for key in keys:
        time.sleep(random.uniform(0.1, 0.3))  # Adjust the range for variation
        element.send_keys(key)


def find_element_by_id_and_click_it_with_javascript(driver, element_identifier):
    _find_element_and_click_it_with_javascript(driver, By.ID, element_identifier)


def find_element_by_xpath_and_click_it_with_javascript(driver, element_identifier):
    _find_element_and_click_it_with_javascript(driver, By.XPATH, element_identifier)


def _find_element_and_click_it_with_javascript(driver, selector_type, element_identifier):
    element = driver.find_element(selector_type, element_identifier)
    driver.execute_script("arguments[0].click();", element)


def _gradually_scroll_element_into_view(driver, element):
    y_offset = 0
    while True:
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(random.uniform(0.2, 0.5))  # Random delay to mimic human behavior
        y_offset += 200
        if y_offset >= element.location['y']:
            break
