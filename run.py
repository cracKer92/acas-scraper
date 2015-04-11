# -*- coding: utf-8 -*-
import requests
import re

from pymongo import MongoClient
from BeautifulSoup import BeautifulSoup
from slugify import slugify
from bson import json_util

import mechanize

# Connect to defualt local instance of MongoClient
client = MongoClient()

# Get database and collection
db = client.arcas

def scrape():

    db.javnenabavke.remove({})

    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]

    search_post_req_url = "http://www.acas.rs/acasPublic/pretragaJavneNabavke.htm"
    search_post_req_payload = {
        'sEcho': 2,
        'iColumns': 8,
        'sColumns': '',
        'iDisplayStart':0,
        'iDisplayLength':10,
        'mDataProp_0':0,
        'mDataProp_1':1,
        'mDataProp_2':2,
        'mDataProp_3':3,
        'mDataProp_4':4,
        'mDataProp_5':5,
        'mDataProp_6':6,
        'mDataProp_7':7,
        'liceId':'',
        'pravnoLiceNaziv':'',
        'tipPostupkaId':'',
        'datumPocetkaOd':'',
        'datumPocetkaDo':'',
        'ishodPostupkaId':'',
        'datumIshodaOd':'',
        'datumIshodaDo':'',
    }

    
    r = requests.post(search_post_req_url, data=search_post_req_payload)
    json_resp = r.json()

    data_list = json_resp['aaData']

    for data in data_list:

        organizacija = data[0]

        podnosilac_izvestaja = data[1]

        tip_postupka = data[2]

        datum_prijema = data[3]

        opis = data[4]

        datum_ishoda = data[5]

        ishod = data[6]
        
        doc = {
            'organizacija': organizacija,
            'podnosilac_izvestaja': podnosilac_izvestaja,
            'tip_postupka':tip_postupka,
            'datum_prijema': datum_prijema,
            'opis': opis,
            'datum_ishoda':datum_ishoda,
            'ishod': ishod
        }

        db.javnenabavke.insert(doc)
                    

            

# Let's scrape.
scrape()