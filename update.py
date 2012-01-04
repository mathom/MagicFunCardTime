#!/usr/bin/env python2.7

import requests
from BeautifulSoup import BeautifulSoup
import re
import sqlite3
import os.path
import atexit

SQL_DB = None

def db_handle():
    global SQL_DB
    if not SQL_DB:
        SQL_DB = sqlite3.connect('magic.db')
        atexit.register(db_close)
    return SQL_DB

def db_close():
    global SQL_DB
    if SQL_DB:
        SQL_DB.close()
    SQL_DB = None

def db_init():
    qry = open('magic.sql', 'r').read()
    conn = db_handle()
    c = conn.cursor()
    c.executescript(qry)
    conn.commit()


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
    dbc = db_handle()
    c = dbc.cursor()
    edition_id = c.execute("SELECT `id` FROM `editions` WHERE `edition` = ?", (edition,)).fetchone()
    if not edition_id:
        c.execute("INSERT INTO `editions` VALUES(NULL, ?)", (edition,))
        dbc.commit()
        edition_id = c.lastrowid
    else:
        edition_id = edition_id[0]
    
    for tr in trs:
        link = tr.findAll('a')[0]
        url = base_url + str(link['href'])

        print "PULLING CARD %s:%s" % (edition, link.text)
        card_id = c.execute('''SELECT `id` FROM `cards` 
                            WHERE `edition_id` = ? AND `name` = ?''',
                            (edition_id, link.text)).fetchone()
        if not card_id:
            c.execute("INSERT INTO `cards` VALUES(NULL, ?, ?)", (edition_id, link.text))
            dbc.commit()

        pull_card(url)
    

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
    try:
        rulings = uls[0]
    except IndexError:
        rulings = None
    try:
        legality = uls[1]
    except IndexError:
        rulings = None
    small = info_td.findNext('td').findChild('small')
    try:
        result["other_parts"] = [x for x in small.findAll('u') if x.text.find('The other part is:') >= 0][0].findNext('a')
    except:
        result["other_parts"] = None
    #try:
    print [x for x in small.findAll('u') if x.text.find('Printings:') >= 0][0].findNext('b')
    #except:
     #   result["printings"] = None
    '''editions
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

