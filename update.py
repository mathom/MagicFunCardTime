#!/usr/bin/env python2.7

import requests
from BeautifulSoup import BeautifulSoup
import re


def scrape(url):
    req = requests.get(url)
    return BeautifulSoup(req.content)


def grab_sets(*names):
    '''returns urls for desired sets'''
    html = scrape('http://magiccards.info/sitemap.html#en')
    english = [x for x in html('h2') if x.text.startswith('English')][0]
    table = english.findNext('table')

    results = []
    for h3 in [x for x in table.findAll('h3') if x.text in names]:
        results += [x['href'] for x in h3.findNext('ul').findAll('a')]

    return results


def pull_set(url):
    '''returns the list of urls'''
    html = scrape(url)
    trs = html.findAll('tr', {"class": 'even'})
    links = [tr.findAll('a') for tr in trs]
#     [pull_card(x) for x in tds if x.t

def pull_card(url):
    pass

if __name__=='__main__':
    updated_sets = grab_sets('Expansions', 'Core Sets')
    print updated_sets

    [pull_set(x) for x in updated_sets]

