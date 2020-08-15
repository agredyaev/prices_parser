from grabber import InputMaker, make_links
from config import Config
import unittest
import sys
import os


sys.path.append(os.getcwd())


class TestInputMaker(unittest.TestCase):

    def test_recieves_link_returns_list_of_links(self):
        url = make_links()[0]
        b = InputMaker(url).make_input()
        self.assertIn(Config.BASE_URL, b[0])
        self.assertIn(Config.BASE_URL, b[3])
        self.assertIn(Config.BASE_URL, b[5])


if __name__ == '__main__':
    unittest.main()
