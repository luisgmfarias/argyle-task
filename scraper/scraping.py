from bs4 import BeautifulSoup
from scraper.navigation import Navigation
import pandas as pd


class Scraping:
    """This class implements reading data from html"""

    navigation = Navigation()
    navigation.login()

    def main_portal_reader(self):
        soup = BeautifulSoup(self.navigation.get_main_portal(), 'lxml')
        job_feed = soup.find('div', {'id': 'feed-jobs'})

        title = []
        url = []
        description = []
        location = []
        tags = []
        client_spendings = []
        payment_status = []
        rating = []

        for sec in job_feed.findAll('section'):
            title.append(sec.find(
                'a', {'class': 'job-title-link'}).getText())

            url.append(
                f"https://upwork.com{sec.find('a', {'class': 'job-title-link'})['href']}")

            description_div = sec.find('div', {'class': 'description'})

            description.append(description_div.find('div',
                                                    {'data-eo-truncation-html-unsafe':
                                                     '::jsuJobDescriptionController.job.description'}
                                                    ).find('span', {'class': 'ng-hide'}).getText())
            tags.append([tag.find('span').getText() for tag in description_div.findAll(
                'a', {'class': 'o-tag-skill'})])

            location.append(sec.find(
                'strong', {'class': 'client-location'}).getText())

            client_spendings.append(sec.find(
                'span', {'class': 'client-spendings'}).getText())

            payment_status.append(sec.find(
                'span', {'class': 'payment-status'}).find('strong').getText())

            rating.append(sec.find(
                'span', {'data-rating-define': 'star'})['data-eo-popover-html-unsafe'])

        return title, url, description, tags, location, client_spendings, payment_status, rating

    def get_data_df(self):

        title, url, description, tags, location, client_spendings, payment_status, rating = self.main_portal_reader()

        works = {
            'title': title,
            'url': url,
            'description': description,
            'tags': tags,
            'location': location,
            'client_spendings': client_spendings,
            'payment_status': payment_status,
            'rating': rating
        }

        df = pd.DataFrame(works, columns=works.keys())
