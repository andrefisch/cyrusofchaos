from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from src.school import School
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

from lxml import html
from flask import Flask, render_template
from io import BytesIO
import requests
import pandas
import operator
import random

import src.scraping_service as ScrapingService

year = ""

# 2016 ARCHIVED VERSION WORKS
# url = "http://web.archive.org/web/20160325002832/http://www.escrimeresults.com/NCAA/NCAA2016.html"
# 2017 WORKS
# url = "https://escrimeresults.com/NCAA/ncaa2017.html"
# 2018 WORKS
# url = "https://escrimeresults.com/NCAA/ncaa2018.html"
# We will see!
url = "https://escrimeresults.com/NCAA/ncaa2019.html"

# year = url[36:40]
year = url[-9:-5]


def get_current_results():
    school_map = _get_school_mappings()
    school_fencers_map = _get_school_fencers_map()

    content = _get_page_content(url=url)

    return ScrapingService.scrape_site_content_ranking_data(
        content=content,
        school_map=school_map,
        school_fencers_map=school_fencers_map,
        year=year)

def get_fencer_numbers():
    school_fencers_map = {}

    with open("./static/text/displayTotal.txt") as f:
        for line in f:
            (key, val) = line.strip('\n').split(";")
            school_fencers_map[key] = val

    school_map = _get_school_mappings()
    schools = []

    for key in school_fencers_map:
        school_name = key
        total_fencers = int(school_fencers_map[school_name])
        total_bouts = total_fencers * 23
        if school_name in school_map:
            school_logo = "%s.png" % school_map[school_name]
        else:
            school_logo = "NCAA.png"

        school = School(school_name,
                        total_fencers,
                        0,
                        0,
                        total_bouts,
                        school_logo)
        schools.append(school)

    return sorted(schools, key=lambda x: (-x.num_fencers, x.name))


def get_school_colors():
    school_colors = {}

    with open("./static/text/schoolColors.txt") as f:
        for line in f:
            (key, color1, color2) = line.strip('\n').split(";")
            school_colors[key] = [color1, color2]

    return school_colors


def _get_school_mappings():
    school_map = {}

    with open("./static/text/schoolDict.txt") as f:
        for line in f:
            (key, val) = line.strip('\n').split(";")
            school_map[key] = val

    return school_map


def _get_school_fencers_map():
    school_fencers_map = {}

    # with open("./static/text/2016TotalFencers.txt") as f:
    # with open("./static/text/2017TotalFencers.txt") as f:
    # with open("./static/text/2018TotalFencers.txt") as f:
    with open("./static/text/2019TotalFencers.txt") as f:
        for line in f:
            (key, val) = line.strip('\n').split(";")
            school_fencers_map[key] = val

    return school_fencers_map


def _get_page_content(url):
    s = requests.Session()
    s.mount('https://', MyAdapter())
    page = s.get(url)

    return pandas.read_html(page.content)
