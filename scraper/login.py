from bs4 import BeautifulSoup
from driver import Driver
import json


class Login:
    """ This class implements the login"""

    start_url = "https://www.upwork.com/ab/account-security/login"
    driver = Driver().init_driver()

    def login(self):
        with open('.login-config.json') as json_file:
            data = json.load(json_file)

        self.driver.get(self.start_url)

        try:
            self.driver.find_element_by_id(
                "login_username"
            ).send_keys(data['login'])

            self.driver.find_element_by_xpath(
                """//*[@button-role="continue"]"""
            ).click()

            self.driver.find_element_by_id(
                "login_password"
            ).send_keys(data['password'])

            self.driver.find_element_by_xpath(
                """//*[@button-role="continue"]"""
            ).click()

        except Exception as e:
            raise e

    def isLogged(self):

        return self.driver.find_element_by_xpath(
            """//*[@id="layout"]/div[2]/div/div[7]/div[3]/div/fe-profile-completeness/div/div[1]/div[2]/h4"""
        ).text == 'My Profile'
