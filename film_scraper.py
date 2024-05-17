# -*- coding: utf-8 -*-
#
# Web scraper

import time
import uuid
import json
import os
import requests
import random
import gzip
import csv
import calendar
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import zlib
import re
import html
from db import open_sqlite, create_page_dump, does_dump_table_exist, url_exists, insert_page
import urllib.request as Request
from urllib.parse import urlparse
from scrapy.exceptions import CloseSpider
# scrapy imports
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.dupefilters import RFPDupeFilter
from scrapy.exceptions import CloseSpider


import logging

def setup_logger():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_folder = os.path.join(os.path.dirname(__name__), "logs")
    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)
        
    log_file = os.path.join(log_folder, f"scraper_log_{current_time}.txt")

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()


def get_random_user_agent():
    agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAARJS; rv:11.0) like Gecko']
    return random.choice(agents)

def is_page_content_valid(url, content):
    """ TODO: detect scraper failure here, e.g. error message in HTML """
    if len(content) == 0: return False
    if len(content) < 10000: return False
    
    # Detect for error message in HTML content for location and critic review pages with no valid data
    '''
    nolocationtext = "It looks like we don't have any filming & production for this title yet."
    nocriticreviewtext = "It looks like we don't have any metacritic reviews for this title yet."

    refine_content = html.unescape(content)
    if (nolocationtext in refine_content) or (nocriticreviewtext in refine_content):
        return False 
    '''
    if "keywords" in url:  
        kw = ["plot keywords", "Contribute to this page",'More from this title','first to contribute']
        for w in kw:
            if not w.lower() in content.lower():
                return False
    return True

_page_counter = 0

class FilmSpider(scrapy.Spider):
    name = 'myspider'
    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,  # seconds, You can adjust download delay if needed
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504],    # default error codes
        'DOWNLOADER_MIDDLEWARES' : {
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            'middleware.CustomRetryMiddleware': 550
        }
    }

    def start_requests(self):
        global _page_counter
        input_file_films = os.path.join(os.path.dirname(__name__), "data/films_to_scrape_sample1.csv")
        with open(input_file_films, 'r') as file:
            logger.info(">>> Reading file + "+input_file_films)
            reader = csv.reader(file)
            for row in reader:
                if row[1] == 'tconst': 
                    continue

                _page_counter = _page_counter + 1
                if _page_counter % 500 == 0:
                    print("\tpage counter = ",_page_counter)

                # store film_id
                self.film_id = row[1]
                
                # get URLs for a film
                urls = [get_base_url(row[1]),
                    get_keyword_url(row[1]), get_synopysis_url(row[1]), 
                    get_location_url(row[1]), get_ratings_url(row[1]), 
                    get_credits_url(row[1]), get_critic_reviews_url(row[1]),
                    get_curated_reviews_url(row[1]), get_curated_reviews_url(row[1]),
                    get_awards_url(row[1])]                                                  
                # scrape urls
                for url in urls:
                    if url_exists(_db, url):
                        #print("URL exists, skipping")
                        continue
                    yield scrapy.Request(url=url,
                                         headers={"User-Agent": get_random_user_agent()},
                                         callback=self.parse, errback=self.error_handler)
                    
    def parse(self, response):
        page_sz = len(response.text)
        logger.debug('   page sz=' + str(page_sz))
        if not is_page_content_valid(response.url, response.text):
            logger.debug('Page content not valid '+response.url)
            raise CloseSpider('error for url, stopping scraper: '+response.url)
        insert_page(_db, response.url, None, response.text, len(response.text))


    def error_handler(self, failure):
        # Log the error
        self.logger.error(repr(failure))
        raise CloseSpider('fatal error for url, stopping scraper: '+failure.request.url)
        # You can optionally handle retries or other actions here
        # For example, retry the failed request:
        # url = failure.request.url
        # yield scrapy.Request(url=url, callback=self.parse, errback=self.error_handler)

def get_base_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/?ref_=ttfc_fc_tt"

def get_keyword_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/keywords/?ref_=tt_stry_kw"

def get_location_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/locations/?ref_=tt_dt_loc"
    
def get_synopysis_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/plotsummary/?ref_=tt_stry_pl"

def get_ratings_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/ratings/?ref_=tt_ov_rt"

def get_credits_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/fullcredits/?ref_=tt_ql_1"

def get_curated_reviews_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/reviews?sort=curated&dir=desc&ratingFilter=0"

def get_upvoted_reviews_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/reviews?sort=totalVotes&dir=desc&ratingFilter=0"

def get_awards_url(film_id):
    assert film_id
    return f"https://www.imdb.com/title/{film_id}/awards/?ref_=tturv_ql_1"

def get_critic_reviews_url(film_id):
    assert film_id
    return f'https://www.imdb.com/title/{film_id}/criticreviews/?ref_=tt_ov_rt'

# FILE: title.basics.tsv.gz
# tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres

_db = open_sqlite(os.path.join(os.path.dirname(__name__), "data/films.db"))
if not does_dump_table_exist(_db):
    create_page_dump(_db)

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'CONCURRENT_REQUESTS': 4  # Adjust the number of concurrent requests here
    })

    process.crawl(FilmSpider)
    process.start()