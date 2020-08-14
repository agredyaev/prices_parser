from config import Config
from driver import *
import unittest
import sys
import os

sys.path.append(os.getcwd())


class TestDriver(unittest.TestCase):

    def test_running_driver_with_options(self):
        with Driver(options='suwgi') as driver:
            driver.load_url(Config.TEST_URL, wait_for_page_body=True)
            selector_start_page = '//*[@class="b-button b-button_disabled_false b-button_theme_catchy b-button_shape_default b-button_size_l b-button_justify_center b-button_selected_false p-index__banner-link"]'
            selector_second_page = '//*[@class="b-accordion__item1"]'
            element_start_page = driver.find_it_by(
                selector_start_page, expected_condition=EC.element_to_be_clickable)
            element_start_page.click()
            element_second_page = driver.find_it_by(selector_second_page)
            self.assertEqual(element_second_page.text, "Все акции")


if __name__ == '__main__':
    unittest.main()
