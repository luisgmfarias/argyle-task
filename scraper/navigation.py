from scraper.driver import Driver
import json
from time import sleep
import random


class Navigation:
    """This class implements all Navigation through the site"""

    def __init__(self):

        self.login_url = "https://www.upwork.com/ab/account-security/login"
        self.driver = Driver().driver()
        self.landing_url = "https://www.upwork.com/ab/find-work/domestic"
        self.contact_info_url = "https://www.upwork.com/freelancers/settings/contactInfo"

    def delay():
        sleep(random.randint(3, 5))

    def login(self):

        self.driver.get(self.landing_url)

        if not self.isLogged():
            with open('.login.json') as json_file:
                data = json.load(json_file)

            try:
                self.delay()

                self.driver.find_element_by_id(
                    "login_username"
                ).send_keys(data['login'])

                self.delay()

                self.driver.find_element_by_xpath(
                    """//*[@button-role="continue"]"""
                ).click()

                self.delay()
                self.driver.find_element_by_id(
                    "login_password"
                ).send_keys(data['password'])

                self.delay()
                self.driver.find_element_by_xpath(
                    """//*[@button-role="continue"]"""
                ).click()

            except Exception as e:
                raise e

    def isLogged(self):

        try:
            self.driver.find_element_by_xpath(
                """//*[@id="layout"]/div[2]/div/div[7]/div[3]/div/fe-profile-completeness/div/div[1]/div[2]/h4"""
            )
            return True
        except:
            return False

    def get_html(self, url):

        if self.driver.current_url != url:
            self.driver.get(url)
            sleep(2)

        return self.driver.page_source

    def get_xhr(self, url):

        self.driver.get(f'view-source:{url}')

        obj = json.loads(self.driver.find_element_by_tag_name('pre').text)

        return obj

    def get_main_portal(self):

        entry_portal_html = self.get_html(url=self.landing_url)

        return entry_portal_html

    def bypass_captcha(self):

        # opening bypass iframe
        externalChallenge = self.driver.find_element_by_id('externalChallenge')
        self.driver.switch_to.frame(externalChallenge)
        captcha_frame = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(captcha_frame)
        self.driver.find_element_by_class_name(
            'recaptcha-checkbox-border').click()

        self.delay()

        # clicking on sound recaptcha button
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(externalChallenge)
        captcha_challenge = self.driver.find_element_by_xpath(
            "//iframe[@title='recaptcha challenge']")
        self.driver.switch_to.frame(captcha_challenge)
        self.driver.find_element_by_id('recaptcha-audio-button').click()

        self.delay()
