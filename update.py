#!/usr/bin/env python2.7

import requests
from BeautifulSoup import BeautifulSoup


def scrape(url):
    req = requests.get(url)
    return BeautifulSoup(req.content)


def grab_sets(*names):
    '''returns urls for desired sets'''
    html = scrape('http://magiccards.info/sitemap.html#en')
    english = [x for x in html('h2') if x.text.startswith('English')][0]
    print repr(english)
    print repr(english.next)
    return []


def pull_set(url):
    '''returns the list of urls'''
    html = scrape(url)
#     tds = html.findAll('td')
    tds = html.findAll('tr', {"class": 'even'})
    [pull_card(x) for x in tds]

def pull_card(url):
    pass

if __name__=='__main__':
    updated_sets = grab_sets('Expansions', 'Core Sets')
    print updated_sets

    [pull_set(x) for x in updated_sets]

