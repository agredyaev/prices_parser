import logging
from driver import *
from time import sleep
from exceptions import *
from datetime import date
from config import Config
from collections import OrderedDict

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s:%(message)s:%(funcName)s')
file_handler = logging.FileHandler('sample.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def make_links(names):
    return [f'{Config.BASE_URL}{city}/retailers' for city in names]


class InputMaker:
    """
    Script crawls retailers for each city
    and makes input depending on the number of offers
    """

    def __init__(self, url):
        self.url = url

    def __get_links_and_number_offers(self):
        with Driver(options=Config.FLAGS) as driver:
            driver.load_url(self.url, wait_on_page=2,
                            wait_for_page_body=True)
            selector = (
                '//*[@class="p-retailers__retailer p-retailers__retailer_empty_false"]'
            )
            elements = driver.find_it_by(
                selector, expected_condition=EC.presence_of_all_elements_located,
                timeout=10)

            hrefs = (elem.get_attribute('href') for elem in elements)
            offers = (elem.get_attribute('text').split()
                      [0] for elem in elements)

            return list(zip(hrefs, offers))

    def make_input(self):
        input = []

        for href, num in self.__get_links_and_number_offers():
            for i in range(1, (int(num) // 30) + 2):
                if 'lenta' not in href:
                    input.append(f'{href}?page={str(i)}')
        return input


class InputParser():
    """Gets offers data from product web_page"""

    def __init__(self, url):
        self.driver = Driver(options=Config.FLAGS)
        self.driver.implicitly_wait(0.1)
        self.url = url

    def __get_elements(self):
        return self.driver.find_it_by(
            '//a[@class="p-retailer__offer"]',
            expected_condition=EC.visibility_of_all_elements_located,
            timeout=30)

    def __parse_segment(self, string):
        chars = ((f'/{a}' if a.isupper() else a) for a in string)
        return ''.join(chars).split('/')[1:]

    def __get_offer_data(self):
        retailer = self.driver.find_it_by(
            '//a[@class="p-offer__retailer"]',
            timeout=10).get_attribute('href').split('/')

        segment = self.driver.find_it_by(
            '//*[@class="p-offer__segment"]', timeout=5).text
        segment = self.__parse_segment(segment)

        try:
            price_old = self.driver.find_it_by(
                '//*[@class="p-offer__price-old"]', timeout=0.05).text
        except Exception:
            price_old = ''

        try:
            discount = self.driver.find_it_by(
                '//*[@class="p-offer__discount"]', timeout=0.05).text
        except Exception:
            discount = ''

        try:
            qty = self.driver.find_it_by(
                '//*[@class="p-offer__quantity"]', timeout=0.05).text
        except Exception:
            qty = ''

        return tuple(OrderedDict(
            create_date=date.today().isoformat(),
            location=retailer[3],
            retailer=retailer[5],
            group=segment[0],
            category='' if len(segment) < 2 else segment[1],
            subcategory='' if len(segment) < 3 else segment[2],
            item_description=self.driver.find_it_by(
                '//*[@class="p-offer__description"]').text,
            price_new=self.driver.find_it_by(
                '//*[@class="p-offer__price-new"]').text,
            price_old=price_old,
            discount=discount,
            qty=qty,
            dates=self.driver.find_it_by(
                '//*[@class="p-offer__dates"]').text
        ).values())

    def __no_items_found(self):
        try:
            return self.driver.find_it_by('//*[@class="b-no-items__root"]',
                                          timeout=2).text
        except:
            return ''

    def get_data(self):
        data = []
        with self.driver as driver:
            driver.load_url(self.url, wait_on_page=1,
                            wait_for_page_body=True)

            if self.__no_items_found():
                raise NoItemsFound()

            else:
                number_elements = len(self.__get_elements())
                for index in range(number_elements):
                    try:
                        elements = self.__get_elements()
                        sleep(0.05)
                        elements[index].click()
                    except WebDriverException:
                        logger.exception(f'{self.url} failed to click element')
                        continue
                    try:
                        offer_data = self.__get_offer_data()
                        data.append(offer_data)
                        driver.back()
                    except WebDriverException:
                        logger.exception(
                            f'{self.url} failed to get data from product page')
                        driver.back()

                return data
