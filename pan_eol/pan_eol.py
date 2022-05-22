#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import prettytable

table = prettytable.PrettyTable(['#', 'Product', 'EOS Date', 'EOL Date', 'Last OS Supported'])
table.align = 'l'
num = 0

data = requests.get('https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates')
soup = BeautifulSoup(data.text, 'html.parser')

data = []
div = soup.find('div', {'class': 'text baseComponent parbase section'})
tbody = div.find('tbody')

for tr in tbody.find_all('tr'):
    if tr.find_all('td'):
        num = num + 1
        product = tr.find_all('td')[0].text.strip()
        eos_date = tr.find_all('td')[1].text.strip()
        eol_date = tr.find_all('td')[2].text.strip()
        os = tr.find_all('td')[4].text.strip()
        table.add_row([num, product, eos_date, eol_date, os])

print(table)
