#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
import requests
import json
import re
from bs4 import BeautifulSoup

app = Flask('__name__')


@app.route('/<int:gross>')
def get_data(gross):
    payload = {'taxman_year': '2016',
               'taxman_vw_1wk': 'on',
               'taxman_vw_mth': 'on',
               'taxman_payperiod': '1',
               'taxman_extra': '',
               'taxman_grosswage': gross,
               'taxman_age': '0',
               'email': '',
               'taxman_vw_yr': 'on'}
    base_url = 'http://www.moneysavingexpert.com/tax-calculator/request/'
    req = requests.post(base_url, data=payload)
    output = json.loads(req.text)['secondOutput']
    soup = BeautifulSoup(output, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    cols = [row.find_all('td') for row in rows[1:]]
    take_home = cols[5][1].string
    take_home_number = re.sub('[£,]', '', take_home)
    return take_home_number


if __name__ == '__main__':
    app.run()
