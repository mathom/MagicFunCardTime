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
    english = html('h2', text=re.compile(r'.*English.*'))[0]
    print repr(english)
    print repr(english.next)
    return []


def pull_set(url):
    '''returns the list of urls'''
    base_url = "http://magiccards.info"
    html = scrape(url)
    trs = html.findAll('tr', {"class": 'even'})
    trs += html.findAll('tr', {"class": 'odd'})
    
    for tr in trs:
        link = tr.findAll('a')[0]
        url = base_url + str(link['href'])
        pull_card(x)
#     urls = [base_url + str(link).split('">')[0][10:] for link in links]
#     [pull_card(x) for x in urls]
    

def pull_card(url):
    pass

if __name__=='__main__':
    updated_sets = grab_sets('Expansions', 'Core Sets')
    print updated_sets

    [pull_set(x) for x in updated_sets]

