from bs4 import BeautifulSoup
from scraper.navigation import Navigation
import pandas as pd
import json
from time import time
from typing import Optional, List
from models.profile import Profile
from models.work import Work
from pydantic import parse_obj_as
import os


class Scraping:
    """This class implements reading data from html"""

    navigation = Navigation()
    navigation.login()

    print('API is Ready')

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
        job_type = []
        tier = []
        date = []

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

            job_type.append(sec.find('strong', {'class': 'js-type'}).getText())

            tier.append(
                sec.find('span', {'class': 'js-contractor-tier'}).getText())

            date.append(
                sec.find('span', {'class': 'js-posted'}).find('time')['datetime'])

        return title, url, description, tags, location, client_spendings, payment_status, rating, job_type, tier, date

    def get_data_df(self):

        title, url, description, tags, location, client_spendings, payment_status, rating, job_type, tier, date = self.main_portal_reader()

        works = {
            'title': title,
            'url': url,
            'description': description,
            'tags': tags,
            'location': location,
            'client_spendings': client_spendings,
            'payment_status': payment_status,
            'rating': rating,
            'job_type': job_type,
            'tier': tier,
            'date': date
        }

        return pd.DataFrame(works, columns=works.keys())

    def save_to_json(self, obj, path: str):

        _, userId = self.get_profile_ids()

        file = f"output/{userId}-{path}-{int(time())}.json"

        os.makedirs(os.path.dirname(file), exist_ok=True)

        with open(file, 'w') as json_file:
            json.dump(obj, json_file, default=str)

        print(f'{str} saved to output file')

    def get_profile_ids(self):
        profile_info = self.navigation.get_xhr(
            'https://www.upwork.com/freelancers/api/v1/profile/me/fwh')
        cipherId = profile_info['identity']['ciphertext']
        userId = profile_info['identity']['userId']

        return cipherId, userId

    def get_profile_obj(self):
        cipherId, _ = self.get_profile_ids()

        url_api_profile = f'https://www.upwork.com/freelancers/api/v1/freelancer/profile/{cipherId}/details?viewMode=1'

        profile_obj = self.navigation.get_xhr(url=url_api_profile)

        return profile_obj

    def get_full_profile_content(self):

        profile_obj = self.get_profile_obj()['profile']

        self.save_to_json(profile_obj, path='full-profile')

        return profile_obj

    def get_portal_content(self):

        df = self.get_data_df()

        portal_objs = json.loads(df.to_json(orient="records"))

        works = parse_obj_as(List[Work], portal_objs)

        works_obj = {'works': [work.dict() for work in works]}

        self.save_to_json(works_obj, path='jobfeed')

        return works_obj

    def get_profile_contact_info(self):

        contact_obj = self.navigation.get_xhr(
            'https://www.upwork.com/freelancers/settings/api/v1/contactInfo')

        return contact_obj

    def get_profile_content(self):

        profile_obj = self.get_profile_obj()
        contact_obj = self.get_profile_contact_info()

        address_data = {
            'line1': contact_obj['freelancer']['address']['street'],
            'line2': contact_obj['freelancer']['address']['additionalInfo'],
            'city': contact_obj['freelancer']['address']['city'],
            'state': contact_obj['freelancer']['address']['state'],
            'postal_code': contact_obj['freelancer']['address']['zip'],
            'country': contact_obj['freelancer']['address']['country']
        }

        profile_data = {
            'id': profile_obj['profile']['identity']['uid'],
            'account': contact_obj['freelancer']['nid'],
            'employer': profile_obj['profile']['employmentHistory'][0]['companyName'],
            'created_at': profile_obj['profile']['stats']['memberSince'],
            'first_name': contact_obj['freelancer']['firstName'],
            'last_name': contact_obj['freelancer']['lastName'],
            'full_name': profile_obj['profile']['profile']['name'],
            'email': contact_obj['freelancer']['email']['address'],
            'phone_number': contact_obj['freelancer']['phone'],
            'picture_url': profile_obj['profile']['profile']['portrait']['portrait'],
            'address': address_data,
        }

        profile = Profile(**profile_data)

        self.save_to_json(profile.dict(), path='profile')

        return profile.dict()
