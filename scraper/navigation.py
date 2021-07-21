from scraper.driver import Driver
import json
from time import sleep


class Navigation:
    """This class implements all Navigation through the site"""

    login_url = "https://www.upwork.com/ab/account-security/login"
    driver = Driver().driver()
    landing_url = "https://www.upwork.com/ab/find-work/domestic"

    def login(self):

        self.driver.get(self.landing_url)

        if not self.isLogged():
            with open('.login.json') as json_file:
                data = json.load(json_file)

            try:
                self.driver.find_element_by_id(
                    "login_username"
                ).send_keys(data['login'])

                sleep(2)

                self.driver.find_element_by_xpath(
                    """//*[@button-role="continue"]"""
                ).click()

                sleep(2)
                self.driver.find_element_by_id(
                    "login_password"
                ).send_keys(data['password'])

                sleep(2)
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

    def get_profile_content(self):

        profile_path = self.driver.find_element_by_xpath(
            """/html/body/div[2]/div/div[2]/div/div[7]/div[3]/div/fe-profile-completeness/div/div[2]/a"""
        ).get_attribute("href")

        profile_html = self.get_html(url=profile_path)

        return profile_html

    def get_main_portal(self):

        entry_portal_html = self.get_html(url=self.landing_url)

        return entry_portal_html
