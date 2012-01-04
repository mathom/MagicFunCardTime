#!/usr/bin/env python2.7

import requests
from BeautifulSoup import BeautifulSoup
import re
import sqlite3
import os.path

def init_db():
    qry = open('magic.sql', 'r').read()
    conn = sqlite3.connect('magic.db')
    c = conn.cursor()
    c.executescript(qry)
    conn.commit()
    c.close()
    conn.close()

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
    base_url = "http://magiccards.info"
    html = scrape(url)
    trs = html.findAll('tr', {"class": 'even'})
    trs.append = html.findAll('tr', {"class": 'odd'})
    links = [tr.findAll('a') for tr in trs]
    urls = [base_url + str(link).split('">')[0][10:] for link in links]
    [pull_card(x) for x in urls]
    

def pull_card(url):
    pass

if __name__=='__main__':

    if not os.path.isfile("magic.db"):
        init_db()

    updated_sets = grab_sets('Expansions', 'Core Sets')
    print updated_sets

    [pull_set(x) for x in updated_sets]

