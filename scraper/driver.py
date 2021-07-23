from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class Driver:

    def driver(self):

        softwares = [SoftwareName.CHROME.value]
        os = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

        user_agent_randomizer = UserAgent(
            software_names=softwares, operating_system=os, limit=100)

        user_agent = user_agent_randomizer.get_random_user_agent()

        # blocked preventions from selenium
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=1420,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--enable-javascript")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(
            executable_path='scraper/chromedriver', chrome_options=options)

        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver
