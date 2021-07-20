from selenium import webdriver
import requests


class Driver:

    def init_driver(self):
        return webdriver.ChromeDriver('chromedriver')

    def current_url(self, driver):
        return requests.get(driver.get_current_url())
