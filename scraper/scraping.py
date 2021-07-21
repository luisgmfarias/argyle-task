from scraper.login import Login
from bs4 import BeautifulSoup
from scraper.driver import Driver


class MainPage():
    """ This class implements a scraping routine through main page"""

    entry = Login()
    driver = Driver()

    def setup(self):

        if not self.entry.isLogged():
            self.entry.login()

    def get_portal_works(self):

        bs = BeautifulSoup(self.driver.current_url)
        feed_jobs = bs.find({'id': 'feed-jobs'})
        for section in feed_jobs.findAll('section'):
            work_title = section.find({'class': 'job-title-link'}).getText()
            work_url = section.find({'class': 'job-title-link'})['href']


class ProfilePage():
    """ This class implements a scraping routine through Profile page"""
