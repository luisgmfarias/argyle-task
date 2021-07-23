from flask import Flask, request
from scraper.scraping import Scraping

app = Flask(__name__)

scrap = Scraping()


@app.route('/profile', methods=['GET'])
def index():
    return scrap.get_profile_content()
