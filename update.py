#!/usr/bin/env python2.7

import requests
from BeautifulSoup import BeautifulSoup
import re


def scrape(url):
    req = requests.get(url)
    return BeautifulSoup(req.content)


def grab_sets(*names):
    '''returns urls for desired sets'''
    url = 'http://magiccards.info/sitemap.html'
    html = scrape(url)
    english = [x for x in html('h2') if x.text.startswith('English')][0]
    table = english.findNext('table')

    results = []
    for h3 in [x for x in table.findAll('h3') if x.text in names]:
        results += [x['href'] for x in h3.findNext('ul').findAll('a')]

    return [url + '/' + x for x in results]


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
    html = scrape(url)

    result = {}
    names = html.findAll('a', {"href": url.replace('http://magiccards.info', '')})
    result["name"] = names[0].text
    info_td = names[0].parent.parent
    info_td_ps = info_td.findAll('p')
    result["card_type"] = info_td_ps[0].text
    ctext = info_td_ps[1].findChild('b').text
    result["illus"] = info_td_ps[3].text

    uls = info_td.findAll('ul')
    rulings = uls[0]
    legality = uls[1]
    small = info_td.findNext('td').findChild('small')
    try:
        result["other_parts"] = small.findNext('u')
    except:
        result["other_parts"] = None
    '''other_parts
    printings
    editions
    cast_cost
    abilities
    powers
    rulings
    legality'''
    return result


if __name__=='__main__':
    updated_sets = grab_sets('Expansions', 'Core Sets')
    print updated_sets
    [pull_set(x) for x in updated_sets]

