import sys

from selenium import webdriver
import unittest
#from webdriver_manager.chrome import ChromeDriverManager

import util

class Test(unittest.TestCase):
    """ Demonstration: Get Chrome to generate fullscreen screenshot """

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1024, 600)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_fullpage_screenshot(self):
        ''' Generate document-height screenshot '''
        url = "http://www.w3schools.com/js/default.asp"
        self.driver.get(url)
        util.fullpage_screenshot(self.driver, "test.png")


if __name__ == "__main__":
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    unittest.main(argv=[sys.argv[0]])
