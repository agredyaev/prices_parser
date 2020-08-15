from time import sleep
from config import Config
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver


class Driver(ChromeDriver):
    """
    Extend ChromeDriver
    \n Options:
    \n h -headless
    \n u -user-agent
    \n p -proxy
    \n w -windos-size
    \n s -no-sandbox
    \n g -disable-gpu
    \n i -incognito
    \n t -num-raster-threads
    """

    def __init__(self, options=''):
        self.options = options

        super(Driver, self).__init__(chrome_options=self.setup_options())

    def load_url(self, url, wait_on_page=0, wait_for_page_body=False):
        """
        Prevent "WebDriverException: Message: waiting for doc.body failed"
        """
        self.get(url)
        if wait_for_page_body:
            self.find_it_by('body', find_by=By.TAG_NAME)
        sleep(wait_on_page)

    def find_it_by(self,
                   selector,
                   find_by=By.XPATH,
                   expected_condition=EC.presence_of_element_located,
                   timeout=30):
        """
        Wait until the element matching the selector appears or timeout.
        """
        return WebDriverWait(self, timeout).until(
            expected_condition((find_by, selector)))

    def setup_options(self):
        chrome_options = ChromeOptions()
        chrome_options.headless = True

        flags = {'h': '--headless',
                 'u': f'user-agent={UserAgent().random}',
                 'p': f'--proxy-server={Config.PROXY}',
                 'w': f'--window-size={Config.WINDOW_SIZE}',
                 's': '--no-sandbox',
                 'g': '--disable-gpu',
                 'i': '--incognito',
                 't': f'--num-raster-threads={Config.THREADS}',
                 '#': '--blink-settings=syncXHRInDocumentsEnabled=false',
                 '@': '--blink-settings=scriptEnabled=false',
                 '%': '--blink-settings=imagesEnabled=false',
                 '$': '--blink-settings=pluginsEnabled=false',
                 'c': '--blink-settings=cookieEnabled=false'}

        if self.options:
            for option in self.options:
                chrome_options.add_argument(flags.get(option, None))

        return chrome_options
