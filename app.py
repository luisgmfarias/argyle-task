from flask import Flask, request
from scraper.scraping import Scraping

app = Flask(__name__)

scrap = Scraping()


@app.route('/profile', methods=['GET'])
def profile():
    return scrap.get_profile_content()


@app.route('/works', methods=['GET'])
def works():
    return scrap.get_portal_content()


@app.route('/full-profile', methods=['GET'])
def full_profile():
    return scrap.get_full_profile_content()
