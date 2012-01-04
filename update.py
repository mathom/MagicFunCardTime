#!/usr/bin/env python2.7

import requests
from BeautifulSoup import BeautifulSoup

def grab_sets(names):
    '''returns urls for desired sets'''
    return []


if __name__=='__main__':
    updated_sets = grab_sets('Expansions', 'Core Sets')

    [pull_set(x) for x in updated_sets]

