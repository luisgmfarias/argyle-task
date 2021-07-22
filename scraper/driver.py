from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class Driver:

    def driver(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        return webdriver.Firefox(executable_path='/home/luis-farias/Documents/argyle-task/scraper/geckodriver')
